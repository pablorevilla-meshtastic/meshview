import argparse
import configparser
import logging
from collections.abc import Mapping
from difflib import get_close_matches
from urllib.parse import urlsplit

logger = logging.getLogger(__name__)

SITE_CONFIG_KEYS = frozenset(
    {
        "domain",
        "language",
        "title",
        "message",
        "announcement",
        "nodes",
        "chat",
        "everything",
        "graphs",
        "stats",
        "net",
        "map",
        "top",
        "api",
        "meshviewworld",
        "map_top_left_lat",
        "map_top_left_lon",
        "map_bottom_right_lat",
        "map_bottom_right_lon",
        "map_interval",
        "map_tile_url",
        "map_tile_attribution",
        "map_tile_max_zoom",
        "map_tile_name",
        "firehose_interval",
        "weekly_net_message",
        "net_tag",
    }
)


DEFAULT_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
DEFAULT_TILE_ATTRIBUTION = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)
DEFAULT_TILE_MAX_ZOOM = 19


def map_tiles(site: Mapping[str, str]) -> dict:
    """Base map tiles for every Leaflet map, from the [site] map_tile_* options.

    Without map_tile_url the maps use OpenStreetMap. A custom tile server (for a
    network without Internet access, or a different map style) gets no attribution
    unless one is configured, is named after its host in the layer picker, and
    replaces the OpenTopoMap layer as well, which would need Internet access.
    """
    url = (site.get("map_tile_url") or "").strip()
    custom = bool(url)
    try:
        max_zoom = int(site.get("map_tile_max_zoom") or DEFAULT_TILE_MAX_ZOOM)
    except ValueError:
        max_zoom = DEFAULT_TILE_MAX_ZOOM
    attribution = (site.get("map_tile_attribution") or "").strip()
    name = (site.get("map_tile_name") or "").strip()
    return {
        "url": url or DEFAULT_TILE_URL,
        "attribution": attribution if custom or attribution else DEFAULT_TILE_ATTRIBUTION,
        "max_zoom": min(max(max_zoom, 1), 22),
        "name": name or ((urlsplit(url).hostname or "Map") if custom else "OpenStreetMap"),
        "custom": custom,
    }


def warn_unknown_site_keys(config: Mapping[str, Mapping[str, str]], config_path: str) -> None:
    """Report ignored site options at startup without logging their values."""
    for key in sorted(set(config.get("site", {})) - SITE_CONFIG_KEYS):
        matches = (
            ["chat"]
            if key == "conversations"
            else get_close_matches(key, sorted(SITE_CONFIG_KEYS), n=1, cutoff=0.8)
        )
        if matches:
            logger.warning(
                "Unknown [site] key %r in %r; this setting is ignored. Did you mean %r?",
                key,
                config_path,
                matches[0],
            )
        else:
            logger.warning(
                "Unknown [site] key %r in %r; this setting is ignored.", key, config_path
            )


# Parse command-line arguments
parser = argparse.ArgumentParser(description="MeshView Configuration Loader")
parser.add_argument(
    "--config", type=str, default="config.ini", help="Path to config.ini file (default: config.ini)"
)
args, _ = parser.parse_known_args()

# Initialize config parser
config_parser = configparser.ConfigParser()
if not config_parser.read(args.config):
    raise FileNotFoundError(f"Config file '{args.config}' not found! Ensure the file exists.")

CONFIG = {section: dict(config_parser.items(section)) for section in config_parser.sections()}
warn_unknown_site_keys(CONFIG, args.config)
