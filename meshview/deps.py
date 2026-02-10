import logging
from importlib.util import find_spec

logger = logging.getLogger(__name__)


def check_optional_deps() -> None:
    if find_spec("pyitm") is None:
        logger.warning(
            "Optional dependency missing: pyitm. "
            "Coverage prediction is disabled. "
            "Run: ./env/bin/pip install -r requirements.txt"
        )
