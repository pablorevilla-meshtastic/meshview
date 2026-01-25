import datetime
import logging
import re
import time

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import IntegrityError

from meshtastic.protobuf.config_pb2 import Config
from meshtastic.protobuf.mesh_pb2 import HardwareModel
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import decode_payload, mqtt_database
from meshview.models import Node, Packet, PacketSeen, Traceroute

logger = logging.getLogger(__name__)


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
                hw_model = (
                    HardwareModel.Name(map_report.hw_model)
                    if hasattr(HardwareModel, "Name")
                    else "unknown"
                )
                role = (
                    Config.DeviceConfig.Role.Name(map_report.role)
                    if hasattr(Config.DeviceConfig.Role, "Name")
                    else "unknown"
                )
                node = (
                    await session.execute(select(Node).where(Node.node_id == node_id))
                ).scalar_one_or_none()

                now_us = int(time.time() * 1_000_000)

                if node:
                    node.node_id = node_id
                    node.long_name = map_report.long_name
                    node.short_name = map_report.short_name
                    node.hw_model = hw_model
                    node.role = role
                    node.channel = env.channel_id
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
                        last_lat=map_report.latitude_i,
                        last_long=map_report.longitude_i,
                        first_seen_us=now_us,
                        last_seen_us=now_us,
                    )
                    session.add(node)
            except Exception as e:
                print(f"Error processing MAP_REPORT_APP: {e}")

            await session.commit()

    if not env.packet.id:
        return

    async with mqtt_database.async_session() as session:
        # --- Packet insert with ON CONFLICT DO NOTHING
        result = await session.execute(select(Packet).where(Packet.id == env.packet.id))
        packet = result.scalar_one_or_none()
        if not packet:
            now_us = int(time.time() * 1_000_000)
            packet_values = {
                "id": env.packet.id,
                "portnum": env.packet.decoded.portnum,
                "from_node_id": getattr(env.packet, "from"),
                "to_node_id": env.packet.to,
                "payload": env.packet.SerializeToString(),
                "import_time_us": now_us,
                "channel": env.channel_id,
            }
            utc_time = datetime.datetime.fromtimestamp(now_us / 1_000_000, datetime.UTC)
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

        # --- PacketSeen (no conflict handling here, normal insert)

        if not env.gateway_id:
            print("WARNING: Missing gateway_id, skipping PacketSeen entry")
            # Most likely a misconfiguration of a mqtt publisher?
            return
        else:
            node_id = int(env.gateway_id[1:], 16)

        result = await session.execute(
            select(PacketSeen).where(
                PacketSeen.packet_id == env.packet.id,
                PacketSeen.node_id == node_id,
                PacketSeen.rx_time == env.packet.rx_time,
            )
        )
        if not result.scalar_one_or_none():
            now_us = int(time.time() * 1_000_000)
            seen = PacketSeen(
                packet_id=env.packet.id,
                node_id=int(env.gateway_id[1:], 16),
                channel=env.channel_id,
                rx_time=env.packet.rx_time,
                rx_snr=env.packet.rx_snr,
                rx_rssi=env.packet.rx_rssi,
                hop_limit=env.packet.hop_limit,
                hop_start=env.packet.hop_start,
                topic=topic,
                import_time_us=now_us,
            )
            session.add(seen)

        # --- NODEINFO_APP handling
        if env.packet.decoded.portnum == PortNum.NODEINFO_APP:
            try:
                user = decode_payload.decode_payload(
                    PortNum.NODEINFO_APP, env.packet.decoded.payload
                )
                if user and user.id:
                    if user.id[0] == "!" and re.fullmatch(r"[0-9a-fA-F]+", user.id[1:]):
                        node_id = int(user.id[1:], 16)
                    else:
                        node_id = None

                    hw_model = (
                        HardwareModel.Name(user.hw_model)
                        if user.hw_model in HardwareModel.values()
                        else f"unknown({user.hw_model})"
                    )
                    role = (
                        Config.DeviceConfig.Role.Name(user.role)
                        if hasattr(Config.DeviceConfig.Role, "Name")
                        else "unknown"
                    )

                    node = (
                        await session.execute(select(Node).where(Node.id == user.id))
                    ).scalar_one_or_none()

                    now_us = int(time.time() * 1_000_000)

                    if node:
                        node.node_id = node_id
                        node.long_name = user.long_name
                        node.short_name = user.short_name
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
                            long_name=user.long_name,
                            short_name=user.short_name,
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
            if position and position.latitude_i and position.longitude_i:
                from_node_id = getattr(env.packet, "from")
                node = (
                    await session.execute(select(Node).where(Node.node_id == from_node_id))
                ).scalar_one_or_none()
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
                        gateway_node_id=int(env.gateway_id[1:], 16),
                        import_time_us=now_us,
                    )
                )

        await session.commit()
