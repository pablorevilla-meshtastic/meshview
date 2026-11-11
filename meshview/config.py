import argparse
import configparser
import logging
from collections.abc import Mapping
from difflib import get_close_matches

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
        "firehose_interval",
        "weekly_net_message",
        "net_tag",
    }
)


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
