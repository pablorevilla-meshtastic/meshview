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
        ({"conversations": "False"}, "false"),
        ({"chat": "False"}, "false"),
        ({"conversations": "True", "chat": "False"}, "true"),
    ],
)
async def test_conversations_option_controls_chat(monkeypatch, site, expected):
    assert (await site_config(monkeypatch, site))["chat"] == expected


@pytest.mark.asyncio
async def test_meshviewworld_option(monkeypatch):
    assert (await site_config(monkeypatch, {}))["meshviewworld"] == "true"
    assert (await site_config(monkeypatch, {"meshviewworld": "False"}))["meshviewworld"] == "false"
