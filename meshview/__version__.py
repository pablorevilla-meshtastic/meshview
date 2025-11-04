"""Version information for MeshView."""

import subprocess
from pathlib import Path

__version__ = "3.0.0"
__release_date__ = "2025-11-05"


def get_git_revision():
    """Get the current git revision hash."""
    try:
        repo_dir = Path(__file__).parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_dir,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_git_revision_short():
    """Get the short git revision hash."""
    try:
        repo_dir = Path(__file__).parent.parent
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_dir,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_version_info():
    """Get complete version information."""
    return {
        "version": __version__,
        "release_date": __release_date__,
        "git_revision": get_git_revision(),
        "git_revision_short": get_git_revision_short(),
    }


# Cache git info at import time for performance
_git_revision = get_git_revision()
_git_revision_short = get_git_revision_short()

# Full version string for display
__version_string__ = f"{__version__} ~ {__release_date__}"
