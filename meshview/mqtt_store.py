import logging
import math
import re
import time
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import IntegrityError

from meshtastic.protobuf.config_pb2 import Config
from meshtastic.protobuf.mesh_pb2 import HardwareModel
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import decode_payload, mqtt_database
from meshview.models import DailySnapshot, Node, Packet, PacketSeen, Traceroute

logger = logging.getLogger(__name__)

MQTT_GATEWAY_CACHE: set[int] = set()
UNKNOWN_NODE_NAME = "unknown name"
NODE_NAME_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")
MQTT_DIRECT_NODE_ID = 1
# Meshtastic node ids are "!" + up to 8 hex digits; be a little lenient on length but the
# result must still fit the BigInteger columns.
NODE_ID_PATTERN = re.compile(r"^!([0-9a-fA-F]{1,16})$")
MAX_NODE_ID = 2**63 - 1


def parse_node_id(value: str | None) -> int | None:
    """Turn a "!deadbeef" style id into an int, or None when it is not one.

    Gateway and user ids arrive over MQTT and are not trustworthy; a malformed one must
    not raise, otherwise the whole ingest loop goes down with it.
    """
    if not value:
        return None
    match = NODE_ID_PATTERN.match(value)
    if not match:
        return None
    node_id = int(match.group(1), 16)
    if node_id > MAX_NODE_ID:
        return None
    return node_id


def has_valid_location(lat: int | None, lon: int | None) -> bool:
    return lat is not None and lon is not None and abs(lat) > 1 and abs(lon) > 1


def node_user_id(node_id: int) -> str:
    return f"!{node_id:0{8}x}"


def placeholder_short_name(node_id: int) -> str:
    return node_user_id(node_id)[-4:]


def normalize_node_name(name: str) -> str:
    name = name.strip()
    if not name or NODE_NAME_CONTROL_CHARS.search(name):
        return UNKNOWN_NODE_NAME
    return name


def storage_packet_id(packet) -> int | None:
    if packet.id:
        return packet.id

    if packet.decoded.portnum != PortNum.MAP_REPORT_APP:
        return None

    from_node_id = getattr(packet, "from", 0) or 0
    now_us = int(time.time() * 1_000_000)
    return -(now_us * 2048 + (from_node_id & 0x7FF))


def storage_to_node_id(packet) -> int:
    if packet.decoded.portnum == PortNum.MAP_REPORT_APP:
        return MQTT_DIRECT_NODE_ID
    return packet.to


async def ensure_node_exists(session, node_id: int | None, channel: str | None) -> Node | None:
    if node_id is None:
        return None

    node = (await session.execute(select(Node).where(Node.node_id == node_id))).scalar_one_or_none()
    now_us = int(time.time() * 1_000_000)

    if node:
        node.last_seen_us = now_us
        if node.first_seen_us is None:
            node.first_seen_us = now_us
        if channel and not node.channel:
            node.channel = channel
        return node

    display_name = str(node_id)
    node = Node(
        id=node_user_id(node_id),
        node_id=node_id,
        long_name=display_name,
        short_name=placeholder_short_name(node_id),
        channel=channel,
        first_seen_us=now_us,
        last_seen_us=now_us,
    )
    session.add(node)
    return node


async def capture_daily_snapshot() -> None:
    """Record packet traffic and active nodes/gateways for the previous UTC day."""
    day_end = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    day_start = day_end - timedelta(days=1)
    start_us = int(day_start.timestamp() * 1_000_000)
    end_us = int(day_end.timestamp() * 1_000_000)
    snapshot_date = day_start.date()

    async with mqtt_database.async_session() as session:
        # Include repeated observations of older packets as activity, too. Node.last_seen_us
        # cannot answer this after a node has already been seen on the following day.
        active_nodes = (
            select(Packet.from_node_id)
            .where(Packet.import_time_us >= start_us, Packet.import_time_us < end_us)
            .union(
                select(Packet.from_node_id)
                .join(PacketSeen, PacketSeen.packet_id == Packet.id)
                .where(PacketSeen.import_time_us >= start_us, PacketSeen.import_time_us < end_us)
            )
            .subquery()
        )
        node_count = (
            await session.execute(select(func.count(active_nodes.c.from_node_id)))
        ).scalar_one()
        packet_count = (
            await session.execute(
                select(func.count())
                .select_from(Packet)
                .where(Packet.import_time_us >= start_us, Packet.import_time_us < end_us)
            )
        ).scalar_one()
        gateway_count = (
            await session.execute(
                select(func.count(func.distinct(PacketSeen.node_id))).where(
                    PacketSeen.import_time_us >= start_us, PacketSeen.import_time_us < end_us
                )
            )
        ).scalar_one()
        captured_at_us = int(time.time() * 1_000_000)
        values = {
            "snapshot_date": snapshot_date,
            "node_count": node_count,
            "packet_count": packet_count,
            "gateway_count": gateway_count,
            "captured_at_us": captured_at_us,
        }

        dialect = session.get_bind().dialect.name
        stmt = None
        if dialect == "sqlite":
            stmt = (
                sqlite_insert(DailySnapshot)
                .values(**values)
                .on_conflict_do_update(index_elements=["snapshot_date"], set_=values)
            )
        elif dialect == "postgresql":
            stmt = (
                pg_insert(DailySnapshot)
                .values(**values)
                .on_conflict_do_update(index_elements=["snapshot_date"], set_=values)
            )

        if stmt is not None:
            await session.execute(stmt)
        else:
            snapshot = (
                await session.execute(
                    select(DailySnapshot).where(DailySnapshot.snapshot_date == snapshot_date)
                )
            ).scalar_one_or_none()
            if snapshot is None:
                session.add(DailySnapshot(**values))
            else:
                snapshot.node_count = node_count
                snapshot.packet_count = packet_count
                snapshot.gateway_count = gateway_count
                snapshot.captured_at_us = captured_at_us

        await session.commit()


async def process_envelope(topic, env):
    # MAP_REPORT_APP
    if env.packet.decoded.portnum == PortNum.MAP_REPORT_APP:
        node_id = getattr(env.packet, "from")
        user_id = f"!{node_id:0{8}x}"

        map_report = decode_payload.decode_payload(
            PortNum.MAP_REPORT_APP, env.packet.decoded.payload
        )

        async with mqtt_database.async_session() as session:
            try:
                hw_model = decode_payload.enum_name(HardwareModel, map_report.hw_model)
                role = decode_payload.enum_name(Config.DeviceConfig.Role, map_report.role)
                node = (
                    await session.execute(select(Node).where(Node.node_id == node_id))
                ).scalar_one_or_none()

                now_us = int(time.time() * 1_000_000)
                has_location = has_valid_location(map_report.latitude_i, map_report.longitude_i)

                if node:
                    node.node_id = node_id
                    node.long_name = map_report.long_name
                    node.short_name = map_report.short_name
                    node.hw_model = hw_model
                    node.role = role
                    if not node.channel:
                        node.channel = env.channel_id
                    if has_location:
                        node.last_lat = map_report.latitude_i
                        node.last_long = map_report.longitude_i
                    node.firmware = map_report.firmware_version
                    node.last_seen_us = now_us
                    if node.first_seen_us is None:
                        node.first_seen_us = now_us
                else:
                    node = Node(
                        id=user_id,
                        node_id=node_id,
                        long_name=map_report.long_name,
                        short_name=map_report.short_name,
                        hw_model=hw_model,
                        role=role,
                        channel=env.channel_id,
                        firmware=map_report.firmware_version,
                        first_seen_us=now_us,
                        last_seen_us=now_us,
                    )
                    if has_location:
                        node.last_lat = map_report.latitude_i
                        node.last_long = map_report.longitude_i
                    session.add(node)
            except Exception as e:
                print(f"Error processing MAP_REPORT_APP: {e}")

            await session.commit()

    packet_id = storage_packet_id(env.packet)
    if packet_id is None:
        return

    async with mqtt_database.async_session() as session:
        # --- Packet insert with ON CONFLICT DO NOTHING
        from_node_id = getattr(env.packet, "from", None)

        result = await session.execute(select(Packet).where(Packet.id == packet_id))
        packet = result.scalar_one_or_none()
        if not packet:
            now_us = int(time.time() * 1_000_000)
            packet_values = {
                "id": packet_id,
                "portnum": env.packet.decoded.portnum,
                "from_node_id": from_node_id,
                "to_node_id": storage_to_node_id(env.packet),
                "payload": env.packet.SerializeToString(),
                "import_time_us": now_us,
                "channel": env.channel_id,
            }
            dialect = session.get_bind().dialect.name
            stmt = None

            if dialect == "sqlite":
                stmt = (
                    sqlite_insert(Packet)
                    .values(**packet_values)
                    .on_conflict_do_nothing(index_elements=["id"])
                )
            elif dialect == "postgresql":
                stmt = (
                    pg_insert(Packet)
                    .values(**packet_values)
                    .on_conflict_do_nothing(index_elements=["id"])
                )

            if stmt is not None:
                await session.execute(stmt)
            else:
                try:
                    async with session.begin_nested():
                        session.add(Packet(**packet_values))
                        await session.flush()
                except IntegrityError:
                    pass

        # --- PacketSeen insert with conflict-safe handling

        gateway_node_id = parse_node_id(env.gateway_id)
        if gateway_node_id is None:
            # Most likely a misconfiguration of a mqtt publisher?
            logger.warning(
                "Skipping PacketSeen entry: missing or malformed gateway_id %r", env.gateway_id
            )
            await session.commit()
            return

        if gateway_node_id not in MQTT_GATEWAY_CACHE:
            MQTT_GATEWAY_CACHE.add(gateway_node_id)
            await session.execute(
                update(Node).where(Node.node_id == gateway_node_id).values(is_mqtt_gateway=True)
            )

        now_us = int(time.time() * 1_000_000)
        seen_values = {
            "packet_id": packet_id,
            "node_id": gateway_node_id,
            "channel": env.channel_id,
            "rx_time": env.packet.rx_time,
            # JSON cannot carry inf/nan, and they are not real SNR readings.
            "rx_snr": env.packet.rx_snr if math.isfinite(env.packet.rx_snr) else None,
            "rx_rssi": env.packet.rx_rssi,
            "hop_limit": env.packet.hop_limit,
            "hop_start": env.packet.hop_start,
            "topic": topic,
            "import_time_us": now_us,
        }
        dialect = session.get_bind().dialect.name
        seen_stmt = None
        if dialect == "sqlite":
            seen_stmt = (
                sqlite_insert(PacketSeen)
                .values(**seen_values)
                .on_conflict_do_nothing(index_elements=["packet_id", "node_id", "rx_time"])
            )
        elif dialect == "postgresql":
            seen_stmt = (
                pg_insert(PacketSeen)
                .values(**seen_values)
                .on_conflict_do_nothing(index_elements=["packet_id", "node_id", "rx_time"])
            )

        if seen_stmt is not None:
            await session.execute(seen_stmt)
        else:
            try:
                async with session.begin_nested():
                    session.add(PacketSeen(**seen_values))
                    await session.flush()
            except IntegrityError:
                pass

        # --- NODEINFO_APP handling
        if env.packet.decoded.portnum == PortNum.NODEINFO_APP:
            try:
                user = decode_payload.decode_payload(
                    PortNum.NODEINFO_APP, env.packet.decoded.payload
                )
                if user and user.id:
                    node_id = parse_node_id(user.id)
                    if node_id is None:
                        logger.warning(
                            "Skipping NODEINFO_APP packet %s: unable to determine node_id",
                            env.packet.id,
                        )
                        await session.commit()
                        return

                    hw_model = decode_payload.enum_name(HardwareModel, user.hw_model)
                    role = decode_payload.enum_name(Config.DeviceConfig.Role, user.role)

                    node = (
                        await session.execute(select(Node).where(Node.id == user.id))
                    ).scalar_one_or_none()
                    if node is None:
                        # The same node may already be stored under a differently
                        # spelled id (e.g. "!00abcd" vs "!abcd"); node_id is unique, so
                        # update that row instead of inserting a duplicate.
                        node = (
                            await session.execute(select(Node).where(Node.node_id == node_id))
                        ).scalar_one_or_none()

                    now_us = int(time.time() * 1_000_000)
                    long_name = normalize_node_name(user.long_name)
                    short_name = normalize_node_name(user.short_name)

                    if node:
                        node.node_id = node_id
                        node.long_name = long_name
                        node.short_name = short_name
                        node.hw_model = hw_model
                        node.role = role
                        node.channel = env.channel_id
                        node.last_seen_us = now_us
                        if node.first_seen_us is None:
                            node.first_seen_us = now_us
                    else:
                        node = Node(
                            id=user.id,
                            node_id=node_id,
                            long_name=long_name,
                            short_name=short_name,
                            hw_model=hw_model,
                            role=role,
                            channel=env.channel_id,
                            first_seen_us=now_us,
                            last_seen_us=now_us,
                        )
                        session.add(node)

            except Exception as e:
                print(f"Error processing NODEINFO_APP: {e}")

        # --- POSITION_APP handling
        if env.packet.decoded.portnum == PortNum.POSITION_APP:
            position = decode_payload.decode_payload(
                PortNum.POSITION_APP, env.packet.decoded.payload
            )
            if position and has_valid_location(position.latitude_i, position.longitude_i):
                node = await ensure_node_exists(
                    session, getattr(env.packet, "from", None), env.channel_id
                )
                if node:
                    now_us = int(time.time() * 1_000_000)
                    node.last_lat = position.latitude_i
                    node.last_long = position.longitude_i
                    node.last_seen_us = now_us
                    if node.first_seen_us is None:
                        node.first_seen_us = now_us
                    session.add(node)

        # --- TRACEROUTE_APP (no conflict handling, normal insert)
        if env.packet.decoded.portnum == PortNum.TRACEROUTE_APP:
            packet_id = env.packet.id
            if packet_id is not None:
                now_us = int(time.time() * 1_000_000)
                session.add(
                    Traceroute(
                        packet_id=packet_id,
                        route=env.packet.decoded.payload,
                        done=not env.packet.decoded.want_response,
                        gateway_node_id=gateway_node_id,
                        import_time_us=now_us,
                    )
                )

        await session.commit()


async def load_gateway_cache():
    async with mqtt_database.async_session() as session:
        result = await session.execute(
            select(Node.node_id).where(Node.is_mqtt_gateway == True)  # noqa: E712
        )
        MQTT_GATEWAY_CACHE.update(result.scalars().all())
