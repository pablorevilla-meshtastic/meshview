import json
import math
from dataclasses import dataclass
from typing import Any

from meshview.config import CONFIG


@dataclass(frozen=True)
class RegionInfo:
    code: str
    freq_start_mhz: float
    freq_end_mhz: float
    spacing_mhz: float
    wide_lora: bool


# Based on Meshtastic firmware `regions[]` in `RadioInterface.cpp`.
REGIONS: dict[str, RegionInfo] = {
    "US": RegionInfo("US", 902.0, 928.0, 0.0, False),
    "EU_433": RegionInfo("EU_433", 433.0, 434.0, 0.0, False),
    "EU_868": RegionInfo("EU_868", 869.4, 869.65, 0.0, False),
    "CN": RegionInfo("CN", 470.0, 510.0, 0.0, False),
    "JP": RegionInfo("JP", 920.5, 923.5, 0.0, False),
    "ANZ": RegionInfo("ANZ", 915.0, 928.0, 0.0, False),
    "ANZ_433": RegionInfo("ANZ_433", 433.05, 434.79, 0.0, False),
    "RU": RegionInfo("RU", 868.7, 869.2, 0.0, False),
    "KR": RegionInfo("KR", 920.0, 923.0, 0.0, False),
    "TW": RegionInfo("TW", 920.0, 925.0, 0.0, False),
    "IN": RegionInfo("IN", 865.0, 867.0, 0.0, False),
    "NZ_865": RegionInfo("NZ_865", 864.0, 868.0, 0.0, False),
    "TH": RegionInfo("TH", 920.0, 925.0, 0.0, False),
    "UA_433": RegionInfo("UA_433", 433.0, 434.7, 0.0, False),
    "UA_868": RegionInfo("UA_868", 868.0, 868.6, 0.0, False),
    "MY_433": RegionInfo("MY_433", 433.0, 435.0, 0.0, False),
    "MY_919": RegionInfo("MY_919", 919.0, 924.0, 0.0, False),
    "SG_923": RegionInfo("SG_923", 917.0, 925.0, 0.0, False),
    "PH_433": RegionInfo("PH_433", 433.0, 434.7, 0.0, False),
    "PH_868": RegionInfo("PH_868", 868.0, 869.4, 0.0, False),
    "PH_915": RegionInfo("PH_915", 915.0, 918.0, 0.0, False),
    "KZ_433": RegionInfo("KZ_433", 433.075, 434.775, 0.0, False),
    "KZ_863": RegionInfo("KZ_863", 863.0, 868.0, 0.0, False),
    "NP_865": RegionInfo("NP_865", 865.0, 868.0, 0.0, False),
    "BR_902": RegionInfo("BR_902", 902.0, 907.5, 0.0, False),
    "LORA_24": RegionInfo("LORA_24", 2400.0, 2483.5, 0.0, True),
    # Firmware UNSET is "Same as US".
    "UNSET": RegionInfo("UNSET", 902.0, 928.0, 0.0, False),
}


def djb2_hash(s: str) -> int:
    """Meshtastic firmware `hash()` (djb2)."""

    h = 5381
    for ch in s:
        h = ((h << 5) + h) + (ord(ch) & 0xFF)
    return h & 0xFFFFFFFF


def _normalize_preset_name(s: str) -> str:
    return "".join(ch for ch in s.upper() if ch.isalnum())


_PRESET_ALIASES: dict[str, str] = {
    "LONGFAST": "LONG_FAST",
    "LONGSLOW": "LONG_SLOW",
    "MEDIUMFAST": "MEDIUM_FAST",
    "MEDIUMSLOW": "MEDIUM_SLOW",
    "SHORTFAST": "SHORT_FAST",
    "SHORTSLOW": "SHORT_SLOW",
    "SHORTTURBO": "SHORT_TURBO",
    "LONGTURBO": "LONG_TURBO",
    "LONGMODERATE": "LONG_MODERATE",
    # Deprecated in firmware enum; treat as LONG_SLOW.
    "VERYLONGSLOW": "VERY_LONG_SLOW",
}


def parse_modem_preset_from_channel_name(channel_name: str) -> str | None:
    if not channel_name:
        return None
    norm = _normalize_preset_name(channel_name)
    return _PRESET_ALIASES.get(norm)


def modem_preset_to_params(preset: str, wide_lora: bool) -> tuple[float, int, int]:
    """Return (bw_khz, sf, cr) matching Meshtastic firmware `modemPresetToParams()`."""

    preset = preset.upper()
    if preset == "SHORT_TURBO":
        return (1625.0 if wide_lora else 500.0, 7, 5)
    if preset == "SHORT_FAST":
        return (812.5 if wide_lora else 250.0, 7, 5)
    if preset == "SHORT_SLOW":
        return (812.5 if wide_lora else 250.0, 8, 5)
    if preset == "MEDIUM_FAST":
        return (812.5 if wide_lora else 250.0, 9, 5)
    if preset == "MEDIUM_SLOW":
        return (812.5 if wide_lora else 250.0, 10, 5)
    if preset == "LONG_TURBO":
        return (1625.0 if wide_lora else 500.0, 11, 8)
    if preset == "LONG_MODERATE":
        return (406.25 if wide_lora else 125.0, 11, 8)
    if preset == "LONG_SLOW":
        return (406.25 if wide_lora else 125.0, 12, 8)
    if preset == "VERY_LONG_SLOW":
        # Enum exists but firmware mapping treats unknown presets as LONG_FAST.
        # Historically this preset has behaved close to LONG_SLOW; keep it stable.
        return (406.25 if wide_lora else 125.0, 12, 8)
    # default: LONG_FAST
    return (812.5 if wide_lora else 250.0, 11, 5)


def get_default_region_code() -> str:
    mqtt_config = CONFIG.get("mqtt", {})
    raw_topics = mqtt_config.get("topics")
    if not raw_topics:
        return "UNSET"

    topics: list[str] = []
    if isinstance(raw_topics, str):
        try:
            loaded = json.loads(raw_topics)
            if isinstance(loaded, list):
                topics = [str(t) for t in loaded]
        except json.JSONDecodeError:
            topics = []

    for t in topics:
        region = parse_region_from_topic(t)
        if region:
            return region

    return "UNSET"


def parse_region_from_topic(topic: str) -> str | None:
    # Expected patterns like: msh/US/bayarea/# or msh/EU_868/somechannel/#
    parts = [p for p in (topic or "").split("/") if p]
    if len(parts) >= 2 and parts[0].lower() == "msh":
        return parts[1]
    return None


def parse_channel_name_from_topic(topic: str) -> str | None:
    parts = [p for p in (topic or "").split("/") if p]
    if len(parts) < 3 or parts[0].lower() != "msh":
        return None

    # Heuristic: channel is the last non-wildcard segment.
    tail = [p for p in parts[2:] if p not in ("#", "+")]
    return tail[-1] if tail else None


def compute_num_channels(region: RegionInfo, bw_khz: float) -> int | None:
    denom = region.spacing_mhz + (bw_khz / 1000.0)
    if denom <= 0:
        return None
    n = math.floor((region.freq_end_mhz - region.freq_start_mhz) / denom)
    return n if n > 0 else None


def compute_frequency_slot(primary_channel_name: str, num_channels: int) -> int:
    """Return 0-based slot index (firmware stores channel_num as 0..numChannels-1)."""

    if num_channels <= 0:
        raise ValueError("num_channels must be > 0")
    return djb2_hash(primary_channel_name) % num_channels


def compute_center_frequency_mhz(region: RegionInfo, bw_khz: float, slot_index: int) -> float:
    # Meshtastic firmware:
    # freq = freqStart + (bw/2000) + (channel_num * (bw/1000))
    # bw is in kHz, freq is in MHz.
    return region.freq_start_mhz + (bw_khz / 2000.0) + slot_index * (bw_khz / 1000.0)


def infer_lora_from_channel_name(
    channel_name: str,
    region_code: str | None = None,
) -> dict[str, Any]:
    region_code = region_code or get_default_region_code()
    region = REGIONS.get(region_code, REGIONS["UNSET"])

    preset = parse_modem_preset_from_channel_name(channel_name) or "LONG_FAST"
    if preset == "VERY_LONG_SLOW":
        # Present in some UIs; treat as LONG_SLOW-compatible.
        preset_for_params = "VERY_LONG_SLOW"
    else:
        preset_for_params = preset

    bw_khz, sf, cr = modem_preset_to_params(preset_for_params, region.wide_lora)
    num_channels = compute_num_channels(region, bw_khz)
    slot_index = None
    slot_1_based = None
    freq_mhz = None
    if channel_name and num_channels:
        slot_index = compute_frequency_slot(channel_name, num_channels)
        slot_1_based = slot_index + 1
        freq_mhz = compute_center_frequency_mhz(region, bw_khz, slot_index)

    return {
        "region": region.code,
        "wide_lora": region.wide_lora,
        "channel_name": channel_name,
        "modem_preset": preset,
        "bw_khz": bw_khz,
        "sf": sf,
        "cr": cr,
        "num_channels": num_channels,
        "frequency_slot": slot_1_based,
        "frequency_slot_index": slot_index,
        "frequency_mhz": freq_mhz,
    }
