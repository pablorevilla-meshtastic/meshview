import datetime
import re
from sqlalchemy import select
from sqlalchemy import update
from meshtastic.protobuf.config_pb2 import Config
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshtastic.protobuf.mesh_pb2 import User, HardwareModel
from meshview import mqtt_database
from meshview import decode_payload
from meshview.models import Packet, PacketSeen, Node, Traceroute


async def process_envelope(topic, env):

    # Checking if the received packet is a MAP_REPORT
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
                    node.last_update = datetime.datetime.now()
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
                        last_update=datetime.datetime.now(),
                    )
                    session.add(node)
            except Exception as e:
                print(f"Error processing MAP_REPORT_APP: {e}")

            await session.commit()

    if not env.packet.id:
        return

    async with mqtt_database.async_session() as session:
        result = await session.execute(
            select(Packet).where(Packet.id == env.packet.id)
        )
        new_packet = False
        packet = result.scalar_one_or_none()
        if not packet:
            new_packet = True
            packet = Packet(
                id=env.packet.id,
                portnum=env.packet.decoded.portnum,
                from_node_id=getattr(env.packet, "from"),
                to_node_id=env.packet.to,
                payload=env.packet.SerializeToString(),
                import_time=datetime.datetime.now(),
                channel=env.channel_id,
            )
            session.add(packet)

        result = await session.execute(
            select(PacketSeen).where(
                PacketSeen.packet_id == env.packet.id,
                PacketSeen.node_id == int(env.gateway_id[1:], 16),
                PacketSeen.rx_time == env.packet.rx_time,
            )
        )
        if not result.scalar_one_or_none():
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
                import_time=datetime.datetime.now(),
            )
            session.add(seen)

        if env.packet.decoded.portnum == PortNum.NODEINFO_APP:
            try:
                user = decode_payload.decode_payload(
                    PortNum.NODEINFO_APP, env.packet.decoded.payload
                )
                if user and user.id:
                    # ✅ Safe fix: only parse hex IDs, otherwise leave None
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
                        await session.execute(
                            select(Node).where(Node.id == user.id)
                        )
                    ).scalar_one_or_none()

                    if node:
                        node.node_id = node_id
                        node.long_name = user.long_name
                        node.short_name = user.short_name
                        node.hw_model = hw_model
                        node.role = role
                        node.channel = env.channel_id
                        node.last_update = datetime.datetime.now()
                    else:
                        node = Node(
                            id=user.id,
                            node_id=node_id,
                            long_name=user.long_name,
                            short_name=user.short_name,
                            hw_model=hw_model,
                            role=role,
                            channel=env.channel_id,
                            last_update=datetime.datetime.now(),
                        )
                        session.add(node)
            except Exception as e:
                print(f"Error processing NODEINFO_APP: {e}")

        if env.packet.decoded.portnum == PortNum.POSITION_APP:
            position = decode_payload.decode_payload(
                PortNum.POSITION_APP, env.packet.decoded.payload
            )
            if position and position.latitude_i and position.longitude_i:
                from_node_id = getattr(env.packet, "from")
                node = (
                    await session.execute(
                        select(Node).where(Node.node_id == from_node_id)
                    )
                ).scalar_one_or_none()
                if node:
                    node.last_lat = position.latitude_i
                    node.last_long = position.longitude_i
                    session.add(node)

        if env.packet.decoded.portnum == PortNum.TRACEROUTE_APP:
            packet_id = None
            if env.packet.decoded.want_response:
                packet_id = env.packet.id
            else:
                result = await session.execute(
                    select(Packet).where(Packet.id == env.packet.decoded.request_id)
                )
                if result.scalar_one_or_none():
                    packet_id = env.packet.decoded.request_id
            if packet_id is not None:
                session.add(
                    Traceroute(
                        packet_id=packet_id,
                        route=env.packet.decoded.payload,
                        done=not env.packet.decoded.want_response,
                        gateway_node_id=int(env.gateway_id[1:], 16),
                        import_time=datetime.datetime.now(),
                    )
                )

        await session.commit()
        if new_packet:
            await packet.awaitable_attrs.to_node
            await packet.awaitable_attrs.from_node
