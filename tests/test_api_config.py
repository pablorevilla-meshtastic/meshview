"""The documented [site] options must reach /api/config."""

import json

import pytest

from meshview.web_api import api


async def site_config(monkeypatch, site):
    monkeypatch.setattr(api, "CONFIG", {"site": site})
    response = await api.api_config(None)
    return json.loads(response.text)["site"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("site", "expected"),
    [
        ({}, "true"),
        ({"conversations": "False"}, "true"),
        ({"chat": "False"}, "false"),
        ({"conversations": "True", "chat": "False"}, "false"),
        ({"conversations": "False", "chat": "True"}, "true"),
    ],
)
async def test_only_chat_option_controls_chat(monkeypatch, site, expected):
    assert (await site_config(monkeypatch, site))["chat"] == expected


@pytest.mark.asyncio
async def test_meshviewworld_option(monkeypatch):
    assert (await site_config(monkeypatch, {}))["meshviewworld"] == "true"
    assert (await site_config(monkeypatch, {"meshviewworld": "False"}))["meshviewworld"] == "false"


@pytest.mark.asyncio
async def test_message_and_announcement(monkeypatch):
    site = await site_config(monkeypatch, {})
    assert site["message"] == "" and site["announcement"] == ""
    site = await site_config(monkeypatch, {"message": "Tagline", "announcement": "Maintenance"})
    assert site["message"] == "Tagline" and site["announcement"] == "Maintenance"


@pytest.mark.asyncio
async def test_default_map_tiles_are_openstreetmap(monkeypatch):
    site = await site_config(monkeypatch, {})
    assert site["map_tile_url"] == "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    assert "OpenStreetMap" in site["map_tile_attribution"]
    assert site["map_tile_name"] == "OpenStreetMap"
    assert site["map_tile_max_zoom"] == 19
    assert site["map_tile_custom"] is False


@pytest.mark.asyncio
async def test_custom_map_tiles(monkeypatch):
    site = await site_config(
        monkeypatch,
        {"map_tile_url": " https://tiles.example.org/{z}/{x}/{y}.png ", "map_tile_max_zoom": "16"},
    )
    assert site["map_tile_url"] == "https://tiles.example.org/{z}/{x}/{y}.png"
    # No credit is assumed for a custom server, and its host names it.
    assert site["map_tile_attribution"] == ""
    assert site["map_tile_name"] == "tiles.example.org"
    assert site["map_tile_max_zoom"] == 16
    assert site["map_tile_custom"] is True


@pytest.mark.asyncio
async def test_custom_map_tiles_name_attribution_and_bad_zoom(monkeypatch):
    site = await site_config(
        monkeypatch,
        {
            "map_tile_url": "http://10.0.0.5/tiles/{z}/{x}/{y}.png",
            "map_tile_name": "Local map",
            "map_tile_attribution": "&copy; OpenStreetMap contributors",
            "map_tile_max_zoom": "deep",
        },
    )
    assert site["map_tile_name"] == "Local map"
    assert site["map_tile_attribution"] == "&copy; OpenStreetMap contributors"
    assert site["map_tile_max_zoom"] == 19
