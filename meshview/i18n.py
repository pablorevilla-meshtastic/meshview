"""Load language catalogs without blocking request handling."""

import asyncio
import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)
LANG_CODE_RE = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})?$")


def _read_catalogs(directory, language):
    directory = Path(directory)
    english = json.loads((directory / "en.json").read_text(encoding="utf-8"))
    if language == "en":
        return english
    try:
        selected = json.loads((directory / f"{language}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        logger.warning("Unable to load language %s; using English", language)
        return english
    # Each section falls back by key, rather than losing all missing translations.
    return {
        section: {**values, **selected.get(section, {})} for section, values in english.items()
    } | {section: values for section, values in selected.items() if section not in english}


async def load_catalogs(directory, language):
    """Return a selected catalog with English defaults for missing keys."""
    if not isinstance(language, str) or not LANG_CODE_RE.fullmatch(language):
        language = "en"
    return await asyncio.to_thread(_read_catalogs, directory, language)
