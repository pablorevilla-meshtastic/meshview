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
    assert config.site_frontend(site) == expected


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
