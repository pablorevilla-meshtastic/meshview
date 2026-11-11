"""Neighbour edges come from each node's latest report in the last 12 hours."""

import json
import time

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshtastic.protobuf.mesh_pb2 import MeshPacket, NeighborInfo
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import database
from meshview.models import Base, Packet
from meshview.web_api import api

HOUR_US = 3600 * 1_000_000


@pytest_asyncio.fixture
async def sessions(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", sessions, raising=False)
    monkeypatch.setattr(api, "_edges_cache", {})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield sessions
    await engine.dispose()


def neighbor_report(row_id, sender, neighbors, hours_ago):
    packet = MeshPacket()
    setattr(packet, "from", sender)
    packet.to = 0xFFFFFFFF
    packet.decoded.portnum = PortNum.NEIGHBORINFO_APP
    info = NeighborInfo(node_id=sender)
    for neighbor in neighbors:
        info.neighbors.add(node_id=neighbor)
    packet.decoded.payload = info.SerializeToString()
    return Packet(
        id=row_id,
        portnum=PortNum.NEIGHBORINFO_APP,
        from_node_id=sender,
        to_node_id=0xFFFFFFFF,
        payload=packet.SerializeToString(),
        import_time_us=int(time.time() * 1_000_000) - int(hours_ago * HOUR_US),
    )


class Request:
    def __init__(self, **query):
        self.query = query


async def edges(**query):
    response = await api.api_edges(Request(**query))
    return {(e["from"], e["to"], e["type"]) for e in json.loads(response.text)["edges"]}


@pytest.mark.asyncio
async def test_neighbor_edges_cover_every_node_in_the_window(sessions):
    # More reporting nodes than the 50 packets the endpoint used to read.
    async with sessions() as session:
        session.add_all(
            neighbor_report(i, 1000 + i, [2000 + i], hours_ago=i / 100) for i in range(80)
        )
        await session.commit()

    found = await edges(type="neighbor")
    assert found == {(2000 + i, 1000 + i, "neighbor") for i in range(80)}


@pytest.mark.asyncio
async def test_latest_report_per_node_and_old_reports_ignored(sessions):
    async with sessions() as session:
        session.add_all(
            [
                neighbor_report(1, 10, [11, 12], hours_ago=1),
                neighbor_report(2, 10, [13], hours_ago=5),  # older report from the same node
                neighbor_report(3, 20, [21], hours_ago=13),  # outside the 12-hour window
            ]
        )
        await session.commit()

    assert await edges() == {(11, 10, "neighbor"), (12, 10, "neighbor")}


@pytest.mark.asyncio
async def test_node_filter_and_cache(sessions):
    async with sessions() as session:
        session.add_all(
            [
                neighbor_report(1, 10, [11], hours_ago=1),
                neighbor_report(2, 20, [21], hours_ago=1),
            ]
        )
        await session.commit()

    assert await edges(node_id="11") == {(11, 10, "neighbor")}

    # A report arriving within the cache minute shows up on the next build.
    async with sessions() as session:
        session.add(neighbor_report(3, 30, [31], hours_ago=0))
        await session.commit()
    assert await edges(node_id="31") == set()
    api._edges_cache.clear()
    assert await edges(node_id="31") == {(31, 30, "neighbor")}


@pytest.mark.asyncio
async def test_bad_parameters(sessions):
    assert await edges(type="other") == set()
    response = await api.api_edges(Request(node_id="x"))
    assert response.status == 400
