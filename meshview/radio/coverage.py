import math
from functools import lru_cache
from typing import List, Tuple

from pyitm.itm import ITM

# ----------------------------
# Config defaults (tune later)
# ----------------------------
DEFAULT_CLIMATE = 5       # Continental temperate
DEFAULT_GROUND = 0.005    # Average ground conductivity
DEFAULT_RELIABILITY = 0.5 # Median
EARTH_RADIUS_KM = 6371.0


def destination_point(lat, lon, bearing_deg, distance_km):
    """
    Compute lat/lon from start point, bearing, distance
    """
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    bearing = math.radians(bearing_deg)

    d = distance_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat1) * math.cos(d)
        + math.cos(lat1) * math.sin(d) * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(d) * math.cos(lat1),
        math.cos(d) - math.sin(lat1) * math.sin(lat2)
    )

    return math.degrees(lat2), math.degrees(lon2)


@lru_cache(maxsize=512)
def compute_coverage(
    lat: float,
    lon: float,
    freq_mhz: float,
    tx_dbm: float,
    tx_height_m: float,
    rx_height_m: float,
    radius_km: float,
    step_km: float,
    reliability: float,
) -> List[Tuple[float, float, float]]:
    """
    Returns list of (lat, lon, rx_dbm)
    Uses ITM area mode (no terrain profile)
    """

    itm = ITM(
        climate=DEFAULT_CLIMATE,
        ground_conductivity=DEFAULT_GROUND,
        refractivity=301,  # standard atmosphere
        freq_mhz=freq_mhz,
        tx_height_m=tx_height_m,
        rx_height_m=rx_height_m,
        polarization=1,  # vertical
        reliability=reliability,
    )

    points = []

    distance = step_km
    while distance <= radius_km:
        for bearing in range(0, 360, 5):
            rx_lat, rx_lon = destination_point(lat, lon, bearing, distance)

            # ITM returns path loss (dB)
            loss_db = itm.path_loss(distance_km=distance)

            rx_dbm = tx_dbm - loss_db

            points.append((rx_lat, rx_lon, rx_dbm))

        distance += step_km

    return points
