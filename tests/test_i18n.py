"""Catalog fallback, UI key coverage, and template rendering across supported languages."""

import json
import re
from html import unescape
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

from meshview.i18n import load_catalogs

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "meshview" / "lang"
LANGUAGES = ("en", "es", "ru")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, f"Duplicate catalog key: {key}"
        result[key] = value
    return result


def read_catalog(language):
    return json.loads((LANG_DIR / f"{language}.json").read_text(), object_pairs_hook=unique_keys)


@pytest.mark.parametrize("language", LANGUAGES)
def test_catalog_coverage_and_placeholders(language):
    english = read_catalog("en")
    selected = read_catalog(language)
    for section, values in english.items():
        assert values.keys() <= selected[section].keys(), (language, section)
        for key, source in values.items():
            if isinstance(source, str):
                assert set(re.findall(r"\{\w+\}", source)) == set(
                    re.findall(r"\{\w+\}", selected[section][key])
                ), (language, section, key)


def test_ui_calls_have_catalog_entries():
    catalog = read_catalog("en")["ui"]
    files = [
        *(ROOT / "meshview" / "templates").glob("*.html"),
        *(ROOT / "meshview" / "static").glob("*.html"),
        *(ROOT / "meshview" / "static").glob("*.js"),
    ]
    for path in files:
        source = path.read_text()
        keys = {
            json.loads(match[1])
            for match in re.finditer(r'(?:MeshI18n\.[th]|\btr)\(("(?:\\.|[^"\\])*")', source)
        }
        keys.update(
            match[1] for match in re.finditer(r"(?:MeshI18n\.[th]|\btr)\('([^']+)'", source)
        )
        keys.update(
            unescape(value)
            for value in re.findall(
                r'data-i18n(?:-(?:title|placeholder|aria-label))?="([^"]+)"', source
            )
        )
        assert keys <= catalog.keys(), (path.name, keys - catalog.keys())
        assert all(catalog[key] == key for key in keys)


@pytest.mark.parametrize("language", LANGUAGES)
def test_all_templates_render(language):
    catalog = read_catalog(language)["ui"]
    env = Environment(
        loader=FileSystemLoader(ROOT / "meshview" / "templates"),
        autoescape=select_autoescape(),
    )
    env.globals.update(
        ui_language=language,
        ui_translations=catalog,
        tr=lambda source: catalog.get(source, source),
    )
    for name in env.list_templates():
        rendered = env.get_template(name).render()
        if '<html lang=' in rendered:
            assert f'<html lang="{language}"' in rendered
        assert '{{ tr(' not in rendered


@pytest.mark.asyncio
async def test_missing_keys_fall_back_without_losing_translations(tmp_path):
    english = {"ui": {"Hello": "Hello", "Goodbye": "Goodbye"}, "base": {"home": "Home"}}
    spanish = {"ui": {"Hello": "Hola"}, "custom": {"label": "Personalizado"}}
    for language, values in (("en", english), ("es", spanish)):
        (tmp_path / f"{language}.json").write_text(json.dumps(values))
    selected = await load_catalogs(tmp_path, "es")
    assert selected["ui"] == {"Hello": "Hola", "Goodbye": "Goodbye"}
    assert selected["base"] == english["base"]
    assert selected["custom"] == spanish["custom"]
    # Neither merging nor future consumers should mutate the fallback file.
    assert json.loads((tmp_path / "en.json").read_text()) == english


@pytest.mark.asyncio
@pytest.mark.parametrize("language", ["missing", "../es", "", None])
async def test_unknown_or_invalid_language_falls_back(tmp_path, language):
    (tmp_path / "en.json").write_text('{"ui": {"Hello": "Hello"}}')
    assert await load_catalogs(tmp_path, language) == {"ui": {"Hello": "Hello"}}


@pytest.mark.asyncio
async def test_language_api_merges_keys_and_invalidates_english_cache(tmp_path, monkeypatch):
    import os
    from types import SimpleNamespace

    from meshview.web_api import api

    english_file = tmp_path / "en.json"
    english_file.write_text('{"ui": {"Hello": "Hello", "Goodbye": "Goodbye"}}')
    (tmp_path / "es.json").write_text('{"ui": {"Hello": "Hola"}}')
    monkeypatch.setattr(api, "LANG_DIR", str(tmp_path))
    monkeypatch.setattr(api, "_LANG_CACHE", {})
    request = SimpleNamespace(query={"lang": "es", "section": "ui"})
    response = await api.api_lang(request)
    assert json.loads(response.body) == {"Hello": "Hola", "Goodbye": "Goodbye"}
    previous_mtime = english_file.stat().st_mtime_ns
    english_file.write_text('{"ui": {"Hello": "Hello", "Goodbye": "Bye"}}')
    os.utime(english_file, ns=(previous_mtime + 1_000_000, previous_mtime + 1_000_000))
    response = await api.api_lang(request)
    assert json.loads(response.body) == {"Hello": "Hola", "Goodbye": "Bye"}
    response = await api.api_lang(SimpleNamespace(query={"lang": "es", "section": "missing"}))
    assert response.status == 404


def test_legacy_translation_hooks_have_english_defaults():
    catalog = read_catalog("en")
    for path in (ROOT / "meshview" / "templates").glob("*.html"):
        section = {"map-view": "map"}.get(path.stem, path.stem)
        if section not in catalog:
            continue
        keys = set(
            re.findall(
                r'data-(?:translate-lang(?:-title)?|translate-aria-label|chat-translate)="([^"]+)"',
                path.read_text(),
            )
        )
        assert keys <= catalog[section].keys(), (path.name, keys - catalog[section].keys())
