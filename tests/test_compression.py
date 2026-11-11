"""API and page responses must be gzipped for browsers that accept it."""

import gzip
import json
import pathlib

import pytest
import pytest_asyncio
from aiohttp import web

from meshview import web as meshview_web

STATIC_DIR = pathlib.Path(meshview_web.__file__).parent / "static"
BIG = {"nodes": [{"long_name": f"Node {i}", "short_name": f"N{i}"} for i in range(200)]}


async def big_json(request):
    return web.json_response(BIG)


async def small_json(request):
    return web.json_response({"ok": True})


async def page(request):
    return web.Response(text="<p>meshview</p>" * 200, content_type="text/html")


async def png(request):
    return web.Response(body=b"\x89PNG" + b"\0" * 4096, content_type="image/png")


@pytest_asyncio.fixture
async def client(aiohttp_client):
    app = web.Application(middlewares=[meshview_web.compress_responses])
    app.router.add_get("/api/big", big_json)
    app.router.add_get("/api/small", small_json)
    app.router.add_get("/page", page)
    app.router.add_get("/image.png", png)
    app.router.add_static("/static/", STATIC_DIR)
    return await aiohttp_client(app, auto_decompress=False)


async def get(client, path, encoding="gzip, deflate, br"):
    return await client.get(path, headers={"Accept-Encoding": encoding})


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/api/big", "/page"])
async def test_large_text_responses_are_gzipped(client, path):
    response = await get(client, path)
    assert response.status == 200
    assert response.headers["Content-Encoding"] == "gzip"
    assert response.headers["Vary"] == "Accept-Encoding"


@pytest.mark.asyncio
async def test_gzipped_json_is_intact(client):
    response = await get(client, "/api/big")
    assert json.loads(gzip.decompress(await response.read())) == BIG


@pytest.mark.asyncio
async def test_plain_for_clients_without_gzip(client):
    response = await get(client, "/api/big", encoding="identity")
    assert "Content-Encoding" not in response.headers
    assert response.headers["Vary"] == "Accept-Encoding"
    assert await response.json() == BIG


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/api/small", "/image.png", "/static/map-dashboard.js"])
async def test_small_binary_and_static_responses_are_left_alone(client, path):
    response = await get(client, path)
    assert response.status == 200
    assert "Content-Encoding" not in response.headers
