"""Messages larger than a mesh node can send are not stored; everything else still is."""

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshtastic.protobuf.mesh_pb2 import Position, RouteDiscovery, User
from meshtastic.protobuf.mqtt_pb2 import MapReport, ServiceEnvelope
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import mqtt_database, mqtt_store
from meshview.models import Base, Node, Packet, PacketSeen, Traceroute

TOPIC = "msh/US/bayarea/2/e/LongFast/!00000002"
TABLES = (Node, Packet, PacketSeen, Traceroute)
BIG = 100_000


@pytest_asyncio.fixture
async def sessions(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(mqtt_database, "async_session", sessions, raising=False)
    monkeypatch.setattr(mqtt_store, "MQTT_GATEWAY_CACHE", set())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield sessions
    await engine.dispose()


def envelope(portnum, payload, packet_id=7, channel_id="LongFast", gateway_id="!00000002"):
    env = ServiceEnvelope(gateway_id=gateway_id, channel_id=channel_id)
    env.packet.id = packet_id
    setattr(env.packet, "from", 123)
    env.packet.to = 0xFFFFFFFF
    env.packet.decoded.portnum = portnum
    env.packet.decoded.payload = payload
    return env


def text_envelope_of_size(size):
    """A text message whose whole envelope is exactly `size` bytes."""
    env = envelope(PortNum.TEXT_MESSAGE_APP, b"")
    for _ in range(4):  # the length prefixes grow with the payload, so close in on it
        missing = size - env.ByteSize()
        env.packet.decoded.payload = b"x" * (len(env.packet.decoded.payload) + missing)
    assert env.ByteSize() == size
    return env


async def row_counts(sessions):
    async with sessions() as session:
        return {
            table.__tablename__: (
                await session.execute(select(func.count()).select_from(table))
            ).scalar_one()
            for table in TABLES
        }


NOTHING = {"node": 0, "packet": 0, "packet_seen": 0, "traceroute": 0}

OVERSIZED = {
    "node info with a huge long name": envelope(
        PortNum.NODEINFO_APP, User(id="!0000007b", long_name="A" * BIG).SerializeToString()
    ),
    "node info with a huge short name": envelope(
        PortNum.NODEINFO_APP, User(id="!0000007b", short_name="A" * BIG).SerializeToString()
    ),
    "map report with a huge long name": envelope(
        PortNum.MAP_REPORT_APP,
        MapReport(
            long_name="A" * BIG, latitude_i=377000000, longitude_i=-1224000000
        ).SerializeToString(),
        packet_id=0,
    ),
    "map report with a huge firmware version": envelope(
        PortNum.MAP_REPORT_APP,
        MapReport(
            firmware_version="A" * BIG, latitude_i=377000000, longitude_i=-1224000000
        ).SerializeToString(),
        packet_id=0,
    ),
    "text message with a huge payload": envelope(PortNum.TEXT_MESSAGE_APP, b"A" * BIG),
    "position from an unknown node with a huge channel name": envelope(
        PortNum.POSITION_APP,
        Position(latitude_i=377000000, longitude_i=-1224000000).SerializeToString(),
        channel_id="A" * BIG,
    ),
    "traceroute with a huge route": envelope(
        PortNum.TRACEROUTE_APP, RouteDiscovery(route=range(BIG // 4)).SerializeToString()
    ),
    "small packet with a huge gateway id": envelope(
        PortNum.TEXT_MESSAGE_APP, b"hi", gateway_id="!" + "0" * BIG
    ),
}


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", OVERSIZED)
async def test_oversized_message_stores_nothing(sessions, kind):
    await mqtt_store.process_envelope(TOPIC, OVERSIZED[kind])
    assert await row_counts(sessions) == NOTHING
    assert mqtt_store.MQTT_GATEWAY_CACHE == set()


@pytest.mark.asyncio
async def test_message_at_the_limit_is_stored_and_one_byte_more_is_not(sessions):
    await mqtt_store.process_envelope(TOPIC, text_envelope_of_size(1025))
    assert await row_counts(sessions) == NOTHING
    largest = text_envelope_of_size(1024)
    await mqtt_store.process_envelope(TOPIC, largest)
    assert await row_counts(sessions) == {**NOTHING, "packet": 1, "packet_seen": 1}
    async with sessions() as session:
        stored = (await session.execute(select(Packet.payload))).scalar_one()
    assert stored == largest.packet.SerializeToString()


@pytest.mark.asyncio
async def test_topic_at_the_limit_is_stored_and_one_character_more_is_not(sessions):
    env = envelope(PortNum.TEXT_MESSAGE_APP, b"hi")
    await mqtt_store.process_envelope("t" * 257, env)
    assert await row_counts(sessions) == NOTHING
    longest = "t" * 256
    await mqtt_store.process_envelope(longest, env)
    async with sessions() as session:
        assert (await session.execute(select(PacketSeen.topic))).scalar_one() == longest


@pytest.mark.asyncio
async def test_ordinary_traffic_is_stored_after_an_oversized_message(sessions):
    await mqtt_store.process_envelope(TOPIC, OVERSIZED["node info with a huge long name"])
    user = User(
        id="!0000007b", long_name="The Highlands (KF6DMA) https://bayme.sh", short_name="HL"
    )
    await mqtt_store.process_envelope(
        TOPIC, envelope(PortNum.NODEINFO_APP, user.SerializeToString(), packet_id=8)
    )
    await mqtt_store.process_envelope(
        TOPIC,
        envelope(
            PortNum.MAP_REPORT_APP,
            MapReport(
                long_name="Map Node",
                short_name="MN",
                firmware_version="2.7.15.567b8ea",
                latitude_i=377000000,
                longitude_i=-1224000000,
            ).SerializeToString(),
            packet_id=0,
        ),
    )
    await mqtt_store.process_envelope(
        TOPIC,
        envelope(
            PortNum.TRACEROUTE_APP, RouteDiscovery(route=[1, 2, 3]).SerializeToString(), packet_id=9
        ),
    )
    assert await row_counts(sessions) == {
        "node": 1,
        "packet": 3,
        "packet_seen": 3,
        "traceroute": 1,
    }
    async with sessions() as session:
        node = (await session.execute(select(Node))).scalar_one()
    assert (node.long_name, node.short_name, node.firmware) == ("Map Node", "MN", "2.7.15.567b8ea")
