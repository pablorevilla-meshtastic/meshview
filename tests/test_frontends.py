"""The site owner's frontend setting applies to every visitor."""

import pytest
from aiohttp import web

from meshview import config
from meshview import web as meshview_web


@pytest.mark.parametrize(
    ("site", "expected"),
    [({}, "modern"), ({"frontend": " CLASSIC "}, "classic"), ({"frontend": "old"}, "modern")],
)
def test_site_frontend(site, expected):
    assert config.site_frontend(site, meshview_web.FRONTENDS) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("frontend", ["modern", "classic"])
async def test_configured_frontend(aiohttp_client, monkeypatch, frontend):
    monkeypatch.setattr(meshview_web, "SITE_FRONTEND", frontend)
    app = web.Application()
    app.add_routes(meshview_web.routes)
    client = await aiohttp_client(app)
    other_frontend = "modern" if frontend == "classic" else "classic"

    for path in (
        "/",
        "/map?zoom=8",
        "/nodelist",
        "/chat",
        "/firehose",
        "/node/123",
        "/packet/123",
        "/nodegraph",
        "/net",
        "/stats",
        "/top",
        "/reliability",
        "/traceroute/123",
    ):
        response = await client.get(
            path,
            params={"frontend": other_frontend},
            cookies={"meshview_frontend": other_frontend},
        )
        assert response.status == 200, path
        assert not response.history
        assert not response.cookies
        assert ('class="mesh-header"' in await response.text()) == (frontend == "modern")

    response = await client.get("/map?kiosk=1")
    assert 'class="mesh-header"' in await response.text()

    if frontend == "classic":
        home = await client.get("/")
        classic_map = await client.get("/map")
        assert await home.text() == await classic_map.text()


@pytest.mark.asyncio
async def test_custom_frontend(aiohttp_client, monkeypatch, tmp_path):
    folder = tmp_path / "compact"
    folder.mkdir()
    (folder / "index.html").write_text("Compact home", encoding="utf-8")
    (folder / "map.html").write_text("Compact map", encoding="utf-8")
    frontends = meshview_web.frontend_environments(meshview_web.env, tmp_path)
    monkeypatch.setattr(meshview_web, "FRONTENDS", frontends)
    monkeypatch.setattr(
        meshview_web, "SITE_FRONTEND", config.site_frontend({"frontend": " Compact "}, frontends)
    )
    app = web.Application()
    app.add_routes(meshview_web.routes)
    client = await aiohttp_client(app)

    assert await (await client.get("/")).text() == "Compact home"
    assert await (await client.get("/map")).text() == "Compact map"
    for path in ("/chat", "/map?kiosk=1"):
        response = await client.get(path)
        assert response.status == 200
        assert 'class="mesh-header"' in await response.text()
