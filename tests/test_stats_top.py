"""/api/stats/top pages in a stable order and can leave out nodes without traffic."""

import json

import pytest
import pytest_asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshview import database
from meshview.models import Base, Node, Packet, PacketSeen
from meshview.web_api import api

# node_id: (channel, packets sent, gateway reports per packet)
TRAFFIC = {1: ("A", 3, 2), 2: ("A", 1, 2), 3: ("B", 2, 1), 4: ("A", 0, 0), 5: ("B", 0, 0)}


@pytest_asyncio.fixture
async def sessions(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", sessions, raising=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with sessions() as session:
        packet_id = 0
        for node_id, (channel, sent, reports) in TRAFFIC.items():
            session.add(Node(id=f"!{node_id:08x}", node_id=node_id, channel=channel))
            for _ in range(sent):
                packet_id += 1
                session.add(Packet(id=packet_id, from_node_id=node_id, import_time_us=1000))
                for gateway in range(reports):
                    session.add(
                        PacketSeen(
                            packet_id=packet_id,
                            node_id=100 + gateway,
                            rx_time=0,
                            hop_limit=3,
                            hop_start=3,
                            import_time_us=1000,
                        )
                    )
        await session.commit()
    yield sessions
    await engine.dispose()


class Request:
    def __init__(self, **query):
        self.query = query


async def top(**query):
    try:
        response = await api.api_stats_top(Request(**query))
    except web.HTTPBadRequest as error:
        return 400, json.loads(error.text)
    return response.status, json.loads(response.text)


def ids(body):
    return [node["node_id"] for node in body["nodes"]]


@pytest.mark.asyncio
async def test_default_keeps_every_node_in_a_stable_order(sessions):
    status, body = await top(limit="10")
    assert status == 200
    assert body["total"] == 5
    # seen, then sent, then node_id: the two silent nodes tie and keep node order.
    assert ids(body) == [1, 3, 2, 4, 5]
    first = await top(limit="2")
    rest = await top(limit="3", offset="2")
    assert ids(first[1]) + ids(rest[1]) == ids(body)


@pytest.mark.asyncio
async def test_active_leaves_out_nodes_without_traffic(sessions):
    status, body = await top(active="true", limit="10")
    assert body["total"] == 3
    assert ids(body) == [1, 3, 2]
    status, body = await top(active="true", channel="A", limit="10")
    assert (body["total"], ids(body)) == (2, [1, 2])
    status, body = await top(active="false", limit="10")
    assert body["total"] == 5


@pytest.mark.asyncio
async def test_bad_active_answers_400(sessions):
    status, body = await top(active="sometimes")
    assert status == 400 and "error" in body
