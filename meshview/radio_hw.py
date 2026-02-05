"""Hardware-related radio inference helpers.

Currently used to infer a reasonable default/max TX power for the coverage
prediction UI and API output.
"""

from __future__ import annotations

from dataclasses import dataclass

MAX_TX_POWER_DBM_CAP = 30.0  # 1W
DEFAULT_TX_POWER_DBM = 20.0


@dataclass(frozen=True)
class TxPowerInfo:
    max_dbm: float | None
    max_dbm_capped: float | None
    source: str | None


# Mapping of MeshView Node.hw_model -> max TX power in dBm.
#
# Notes:
# - Values are best-effort. Some devices don't have explicit max-TX-power
#   documentation; for those we pick a conservative chip-typical max.
# - Output should always be capped at 30 dBm (1W) per project requirement.
HW_MAX_TX_POWER_DBM: dict[str, tuple[float, str]] = {
    # Heltec
    "HELTEC_V4": (28.0, "https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/"),
    # B&Q / Unit Engineering
    # Docs mention an additional 35 dBm PA; cap to 30 dBm.
    "STATION_G2": (
        35.0,
        "https://meshtastic.org/docs/hardware/devices/b-and-q-consulting/station-series/",
    ),
    "STATION_G1": (
        35.0,
        "https://meshtastic.org/docs/hardware/devices/b-and-q-consulting/station-series/",
    ),
}


def _normalize_hw_model(hw_model: str | None) -> str | None:
    if not hw_model:
        return None
    s = str(hw_model).strip()
    return s.upper() if s else None


def infer_max_tx_power_dbm(hw_model: str | None) -> TxPowerInfo:
    """Infer a best-effort max TX power for a given hw_model.

    Returns both the raw inferred max and the capped max.
    """

    model = _normalize_hw_model(hw_model)
    if not model:
        return TxPowerInfo(DEFAULT_TX_POWER_DBM, DEFAULT_TX_POWER_DBM, "default")

    explicit = HW_MAX_TX_POWER_DBM.get(model)
    if explicit:
        raw, source = explicit
        capped = min(float(raw), MAX_TX_POWER_DBM_CAP)
        return TxPowerInfo(float(raw), capped, source)

    # Unknown/variable boards: default to 20 dBm unless we have explicit docs.
    return TxPowerInfo(DEFAULT_TX_POWER_DBM, DEFAULT_TX_POWER_DBM, "default")
