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
        ({"conversations": "True", "chat": "False"}, "false"),
        ({"conversations": "False", "chat": "True"}, "true"),
    ],
)
async def test_chat_option_takes_priority_over_legacy_conversations(monkeypatch, site, expected):
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
