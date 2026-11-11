"""/api/nodes keeps its historical answer and adds paging, sorting, search and facets."""

import json
import time

import pytest
import pytest_asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshview import database
from meshview.models import Base, Node
from meshview.web_api import api

NOW_US = int(time.time() * 1_000_000)
DAY_US = 86_400 * 1_000_000

# node_id, short_name, long_name, role, channel, hw_model, firmware, lat, long, altitude,
# gateway, days since last seen
NODES = [
    (1, "beta", "Beta Base", "ROUTER", "LongFast", "RAK4631", "2.7.1", 1, 1, 300, True, 0),
    (2, "Alfa", "alfa 50% off", "CLIENT", "LongFast", "HELTEC_V3", "2.7.1", 0, 0, None, False, 1),
    (3, "Gamma", "Gamma Hill", "ROUTER", "MediumFast", "RAK4631", None, 2, 2, 900, None, 2),
    (4, "delta", "Delta", "CLIENT", "LongFast", "HELTEC_V3", "2.6.0", None, None, 10, False, 10),
    (5, "Alfa", "Alfa Two", "CLIENT_MUTE", "LongFast", "T_ECHO", "2.7.1", 3, 3, None, True, 20),
]


@pytest_asyncio.fixture
async def sessions(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", sessions, raising=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with sessions() as session:
        for node_id, short, long_, role, channel, hw, fw, lat, lon, alt, gw, days in NODES:
            session.add(
                Node(
                    id=f"!{node_id:08x}",
                    node_id=node_id,
                    short_name=short,
                    long_name=long_,
                    role=role,
                    channel=channel,
                    hw_model=hw,
                    firmware=fw,
                    last_lat=lat,
                    last_long=lon,
                    last_altitude=alt,
                    is_mqtt_gateway=gw,
                    first_seen_us=NOW_US - 30 * DAY_US,
                    last_seen_us=NOW_US - days * DAY_US - 1000,
                )
            )
        # Never seen: always left out.
        session.add(Node(id="!00000063", node_id=99, short_name="zz"))
        await session.commit()
    yield sessions
    await engine.dispose()


class Request:
    def __init__(self, **query):
        self.query = query


async def call(handler, **query):
    try:
        response = await handler(Request(**query))
    except web.HTTPBadRequest as error:
        return 400, json.loads(error.text)
    return response.status, json.loads(response.text)


async def nodes(**query):
    status, body = await call(api.api_nodes, **query)
    assert status == 200, body
    return body


def ids(body):
    return [node["node_id"] for node in body["nodes"]]


@pytest.mark.asyncio
async def test_historical_answer_is_unchanged(sessions):
    body = await nodes()
    assert set(body) == {"nodes"}  # no paging keys unless asked for
    # short_name as stored (uppercase first), ties on node_id.
    assert ids(body) == [2, 5, 3, 1, 4]
    assert list(body["nodes"][0]) == list(api.NODE_FIELDS)
    assert ids(await nodes(days_active="3")) == [2, 3, 1]
    assert ids(await nodes(days_active="abc")) == [2, 5, 3, 1, 4]
    assert ids(await nodes(days_active="")) == [2, 5, 3, 1, 4]
    assert ids(await nodes(role="router")) == [3, 1]
    assert ids(await nodes(channel="LongFast", hw_model="HELTEC_V3")) == [2, 4]
    assert ids(await nodes(node_id="3")) == [3]


@pytest.mark.asyncio
async def test_sort_is_case_insensitive_with_missing_values_last(sessions):
    assert ids(await nodes(sort="short_name")) == [2, 5, 1, 4, 3]
    assert ids(await nodes(sort="-short_name")) == [3, 4, 1, 2, 5]
    assert ids(await nodes(sort="-last_altitude")) == [3, 1, 4, 2, 5]
    assert ids(await nodes(sort="last_altitude")) == [4, 1, 3, 2, 5]
    assert ids(await nodes(sort="firmware")) == [4, 1, 2, 5, 3]


@pytest.mark.asyncio
async def test_pages_follow_each_other(sessions):
    first = await nodes(sort="long_name", limit="2")
    second = await nodes(sort="long_name", limit="2", offset="2")
    rest = await nodes(sort="long_name", limit="2", offset="4")
    assert (first["total"], first["limit"], first["offset"]) == (5, 2, 0)
    assert ids(first) + ids(second) + ids(rest) == ids(await nodes(sort="long_name"))
    assert ids(await nodes(limit="0")) == [2]  # clamped to one
    assert (await nodes(offset="3"))["total"] == 5


@pytest.mark.asyncio
async def test_filters(sessions):
    assert ids(await nodes(firmware="2.7.1")) == [2, 5, 1]
    assert ids(await nodes(ids="4,1,77")) == [1, 4]
    assert ids(await nodes(ids="")) == []
    assert ids(await nodes(is_mqtt_gateway="true")) == [5, 1]
    assert ids(await nodes(is_mqtt_gateway="false")) == [2, 3, 4]
    # Zero coordinates count as no position, as on the map.
    assert ids(await nodes(has_position="true")) == [5, 3, 1]
    assert ids(await nodes(has_position="false")) == [2, 4]


@pytest.mark.asyncio
async def test_search(sessions):
    assert ids(await nodes(search="ALFA")) == [2, 5]
    assert ids(await nodes(search="hill")) == [3]
    assert ids(await nodes(search="!00000004")) == [4]
    assert ids(await nodes(search="00000004")) == [4]
    assert ids(await nodes(search="5")) == [2, 5]  # "50% off" and node 5
    # LIKE wildcards are matched literally.
    assert ids(await nodes(search="50%")) == [2]
    assert ids(await nodes(search="_")) == []


@pytest.mark.asyncio
async def test_fields(sessions):
    body = await nodes(fields="short_name,last_seen_us", limit="1")
    assert list(body["nodes"][0]) == ["node_id", "short_name", "last_seen_us"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query",
    [
        {"sort": "password"},
        {"sort": "-"},
        {"limit": "ten"},
        {"offset": "x"},
        {"ids": "1,two"},
        {"ids": ",".join(["1"] * 501)},
        {"fields": "short_name,secret"},
        {"is_mqtt_gateway": "maybe"},
        {"has_position": "2"},
        {"search": "x" * 101},
    ],
)
async def test_bad_parameters_answer_400(sessions, query):
    status, body = await call(api.api_nodes, **query)
    assert status == 400 and "error" in body


@pytest.mark.asyncio
async def test_facets(sessions):
    status, body = await call(api.api_node_facets, days_active="3")
    assert status == 200
    assert body["total"] == 3
    assert body["facets"]["role"] == [
        {"value": "ROUTER", "count": 2},
        {"value": "CLIENT", "count": 1},
    ]
    assert {"value": None, "count": 1} in body["facets"]["firmware"]

    status, body = await call(api.api_node_facets, is_mqtt_gateway="true")
    assert body["total"] == 2
    assert body["facets"]["channel"] == [{"value": "LongFast", "count": 2}]

    status, body = await call(api.api_node_facets, has_position="maybe")
    assert status == 400
