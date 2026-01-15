import argparse
import configparser

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
