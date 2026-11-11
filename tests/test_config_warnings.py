"""Unknown site options should be visible at startup rather than silently ignored."""

import configparser
import logging
import subprocess
import sys
from pathlib import Path

import pytest

from meshview import config


@pytest.mark.parametrize("settings", [{}, {"site": {}}, {"site": {"chat": "False"}}])
def test_supported_and_missing_site_options_do_not_warn(caplog, settings):
    with caplog.at_level(logging.WARNING, logger="meshview.config"):
        config.warn_unknown_site_keys(settings, "custom.ini")
    assert not caplog.records


def test_unknown_keys_warn_with_filename_and_spelling_hint(caplog):
    with caplog.at_level(logging.WARNING, logger="meshview.config"):
        config.warn_unknown_site_keys(
            {"site": {"firehose_interal": "sensitive-value", "starting": "/chat"}},
            "custom.ini",
        )
    assert len(caplog.records) == 2
    assert "'firehose_interal'" in caplog.text
    assert "Did you mean 'firehose_interval'?" in caplog.text
    assert "'starting'" in caplog.text
    assert "'custom.ini'" in caplog.text
    assert "sensitive-value" not in caplog.text
    assert "/chat" not in caplog.text


def test_untrusted_key_cannot_add_log_lines(caplog):
    with caplog.at_level(logging.WARNING, logger="meshview.config"):
        config.warn_unknown_site_keys({"site": {"unknown\nforged": "ignored"}}, "custom.ini")
    assert "unknown\\nforged" in caplog.records[0].getMessage()
    assert "\n" not in caplog.records[0].getMessage()


@pytest.mark.parametrize("filename", ["sample.config.ini", "container/config.ini"])
def test_shipped_site_options_are_recognized(caplog, filename):
    parser = configparser.ConfigParser()
    parser.read(Path(__file__).resolve().parents[1] / filename)
    settings = {section: dict(parser.items(section)) for section in parser.sections()}
    with caplog.at_level(logging.WARNING, logger="meshview.config"):
        config.warn_unknown_site_keys(settings, filename)
    assert not caplog.records


def test_startup_checks_the_selected_config_file(tmp_path):
    filename = tmp_path / "custom.ini"
    filename.write_text("[site]\nCHAT = False\nfirehose_interal = 10\n")
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from meshview.config import CONFIG; print(CONFIG['site']['chat'])",
            "--config",
            str(filename),
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "False"
    assert "firehose_interal" in result.stderr
    assert "Did you mean 'firehose_interval'?" in result.stderr
    assert str(filename) in result.stderr
    assert "Unknown [site] key 'chat'" not in result.stderr


@pytest.mark.asyncio
async def test_site_keys_read_by_api_are_recognized(monkeypatch):
    from meshview.web_api import api

    keys = set()

    class SiteSettings(dict):
        def get(self, key, default=None):
            keys.add(key)
            return super().get(key, default)

    monkeypatch.setattr(api, "CONFIG", {"site": SiteSettings()})
    response = await api.api_config(None)
    assert response.status == 200
    assert keys <= config.SITE_CONFIG_KEYS


def test_removed_conversations_key_warns_and_suggests_chat(caplog):
    with caplog.at_level(logging.WARNING, logger="meshview.config"):
        config.warn_unknown_site_keys({"site": {"conversations": "False"}}, "custom.ini")
    assert "Unknown [site] key 'conversations'" in caplog.text
    assert "Did you mean 'chat'?" in caplog.text
