"""A node's channel comes from the node info it broadcasts, not from one sent to a single node."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshtastic.protobuf.mesh_pb2 import User
from meshtastic.protobuf.mqtt_pb2 import ServiceEnvelope
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import mqtt_database, mqtt_store
from meshview.models import Base, Node

NODE = 0x1234ABCD
OTHER = 0x0BADCAFE
BROADCAST = 0xFFFFFFFF


def node_info(packet_id, channel, to):
    env = ServiceEnvelope(gateway_id="!00000002", channel_id=channel)
    env.packet.id = packet_id
    setattr(env.packet, "from", NODE)
    env.packet.to = to
    env.packet.decoded.portnum = PortNum.NODEINFO_APP
    user = User(id=f"!{NODE:08x}", long_name="Node", short_name="NODE")
    env.packet.decoded.payload = user.SerializeToString()
    return env


@pytest.mark.asyncio
async def test_directed_node_info_keeps_the_channel(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(mqtt_database, "async_session", sessions, raising=False)
    monkeypatch.setattr(mqtt_store, "MQTT_GATEWAY_CACHE", set())

    async def channel():
        async with sessions() as session:
            node = (await session.execute(select(Node).where(Node.node_id == NODE))).scalar_one()
            return node.channel

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # Directed, to a node it has just found: a node with no channel yet takes it.
        await mqtt_store.process_envelope("test", node_info(1, "Secondary", OTHER))
        assert await channel() == "Secondary"
        # Broadcast on its primary channel: that is its channel.
        await mqtt_store.process_envelope("test", node_info(2, "LongFast", BROADCAST))
        assert await channel() == "LongFast"
        # Directed again, on a secondary channel: the channel stays.
        await mqtt_store.process_envelope("test", node_info(3, "Secondary", OTHER))
        assert await channel() == "LongFast"
        # A broadcast on another channel means it moved.
        await mqtt_store.process_envelope("test", node_info(4, "MediumFast", BROADCAST))
        assert await channel() == "MediumFast"
    finally:
        await engine.dispose()
