"""/api/packets pages back in time with before and next_before."""

import json

import pytest
import pytest_asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshtastic.protobuf.mesh_pb2 import MeshPacket
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import database, models
from meshview import web as meshview_web
from meshview.web_api import api


def packet(row_id, time_us, portnum=PortNum.POSITION_APP, text=b""):
    mesh = MeshPacket(id=row_id)
    setattr(mesh, "from", 123)
    mesh.to = 0xFFFFFFFF
    mesh.decoded.portnum = portnum
    mesh.decoded.payload = text
    return models.Packet(
        id=row_id,
        from_node_id=123,
        to_node_id=0xFFFFFFFF,
        portnum=portnum,
        channel="Main",
        payload=mesh.SerializeToString(),
        import_time_us=time_us,
    )


@pytest_asyncio.fixture
async def sessions(monkeypatch):
    api.init_api_module(meshview_web.Packet, meshview_web.SEQ_REGEX, meshview_web.LANG_DIR)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", sessions)
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield sessions
    await engine.dispose()


class Request:
    def __init__(self, **query):
        self.query = query


async def call(**query):
    try:
        response = await api.api_packets(Request(**query))
    except web.HTTPBadRequest as error:
        return 400, json.loads(error.text)
    return response.status, json.loads(response.text)


@pytest.mark.asyncio
async def test_pages_follow_each_other(sessions):
    async with sessions() as session:
        session.add_all(packet(i, i * 100) for i in range(1, 8))
        await session.commit()

    status, first = await call(node_id="123", limit="3")
    assert status == 200
    assert [p["id"] for p in first["packets"]] == [7, 6, 5]
    assert first["next_before"] == 500

    status, second = await call(node_id="123", limit="3", before=str(first["next_before"]))
    assert [p["id"] for p in second["packets"]] == [4, 3, 2]

    status, last = await call(node_id="123", limit="3", before=str(second["next_before"]))
    assert [p["id"] for p in last["packets"]] == [1]
    assert "next_before" not in last  # nothing older


@pytest.mark.asyncio
async def test_cursor_survives_filtered_text_messages(sessions):
    async with sessions() as session:
        session.add_all(
            [
                packet(1, 100, PortNum.TEXT_MESSAGE_APP, b"hello"),
                # Sequence-number messages are dropped after the query.
                packet(2, 200, PortNum.TEXT_MESSAGE_APP, b"seq 41"),
                packet(3, 300, PortNum.TEXT_MESSAGE_APP, b"seq 42"),
            ]
        )
        await session.commit()

    status, first = await call(portnum="1", limit="2")
    assert first["packets"] == []  # both rows read were filtered out...
    assert first["next_before"] == 200  # ...but the next page still starts after them

    status, second = await call(portnum="1", limit="2", before="200")
    assert [p["payload"] for p in second["packets"]] == ["hello"]


@pytest.mark.asyncio
async def test_bad_before_answers_400(sessions):
    status, body = await call(before="yesterday")
    assert status == 400 and "error" in body
