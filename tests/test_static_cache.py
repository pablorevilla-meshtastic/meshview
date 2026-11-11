"""Static files must tell browsers how long they may reuse them."""

import pathlib

import pytest
import pytest_asyncio
from aiohttp import web

from meshview import web as meshview_web

STATIC_DIR = pathlib.Path(meshview_web.__file__).parent / "static"


async def ping(request):
    return web.json_response({"ok": True})


@pytest_asyncio.fixture
async def client(aiohttp_client):
    app = web.Application()
    app.on_response_prepare.append(meshview_web.set_static_cache_headers)
    app.router.add_static("/static/", STATIC_DIR)
    app.router.add_get("/api/ping", ping)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_own_files_are_revalidated(client):
    response = await client.get("/static/map-dashboard.js")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "no-cache"

    # Revalidating an unchanged file costs a 304 without the body.
    again = await client.get(
        "/static/map-dashboard.js", headers={"If-None-Match": response.headers["ETag"]}
    )
    assert again.status == 304
    assert again.headers["Cache-Control"] == "no-cache"


@pytest.mark.asyncio
async def test_versioned_vendor_files_are_cached_for_good(client):
    response = await client.get("/static/vendor/leaflet-1.9.4/dist/leaflet.js")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "public, max-age=31536000, immutable"


@pytest.mark.asyncio
async def test_unversioned_vendor_files_are_revalidated(client):
    response = await client.get("/static/vendor/manifest.json")
    assert response.status == 200
    assert response.headers["Cache-Control"] == "no-cache"


@pytest.mark.asyncio
async def test_other_routes_are_left_alone(client):
    response = await client.get("/api/ping")
    assert "Cache-Control" not in response.headers
