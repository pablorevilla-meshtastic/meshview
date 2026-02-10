import math
from functools import lru_cache

try:
    from pyitm import itm

    ITM_AVAILABLE = True
except Exception:
    itm = None
    ITM_AVAILABLE = False

DEFAULT_CLIMATE = 5  # Continental temperate
DEFAULT_GROUND = 0.005  # Average ground conductivity
DEFAULT_EPS_DIELECT = 15.0
DEFAULT_DELTA_H = 90.0
DEFAULT_RELIABILITY = 0.5
DEFAULT_MIN_DBM = -130.0
DEFAULT_MAX_DBM = -80.0
DEFAULT_THRESHOLD_DBM = -120.0
EARTH_RADIUS_KM = 6371.0
BEARING_STEP_DEG = 5


def destination_point(
    lat: float, lon: float, bearing_deg: float, distance_km: float
) -> tuple[float, float]:
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    bearing = math.radians(bearing_deg)

    d = distance_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(d) * math.cos(lat1),
        math.cos(d) - math.sin(lat1) * math.sin(lat2),
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
) -> list[tuple[float, float, float]]:
    if not ITM_AVAILABLE:
        return []
    points = []
    distance = max(step_km, 1.0)
    while distance <= radius_km:
        for bearing in range(0, 360, BEARING_STEP_DEG):
            rx_lat, rx_lon = destination_point(lat, lon, bearing, distance)
            try:
                loss_db, _ = itm.area(
                    ModVar=2,  # Mobile: pctTime=reliability, pctConf=confidence
                    deltaH=DEFAULT_DELTA_H,
                    tht_m=tx_height_m,
                    rht_m=rx_height_m,
                    dist_km=distance,
                    TSiteCriteria=0,
                    RSiteCriteria=0,
                    eps_dielect=DEFAULT_EPS_DIELECT,
                    sgm_conductivity=DEFAULT_GROUND,
                    eno_ns_surfref=301,
                    frq_mhz=freq_mhz,
                    radio_climate=DEFAULT_CLIMATE,
                    pol=1,
                    pctTime=reliability,
                    pctLoc=0.5,
                    pctConf=0.5,
                )
                rx_dbm = tx_dbm - loss_db
                points.append((rx_lat, rx_lon, rx_dbm))
            except itm.InputError:
                continue
        distance += step_km

    return points


@lru_cache(maxsize=512)
def compute_perimeter(
    lat: float,
    lon: float,
    freq_mhz: float,
    tx_dbm: float,
    tx_height_m: float,
    rx_height_m: float,
    radius_km: float,
    step_km: float,
    reliability: float,
    threshold_dbm: float,
) -> list[tuple[float, float]]:
    if not ITM_AVAILABLE:
        return []
    perimeter = []
    distance = max(step_km, 1.0)
    for bearing in range(0, 360, BEARING_STEP_DEG):
        last_point = None
        last_rx_dbm = None
        dist = distance
        while dist <= radius_km:
            try:
                loss_db, _ = itm.area(
                    ModVar=2,
                    deltaH=DEFAULT_DELTA_H,
                    tht_m=tx_height_m,
                    rht_m=rx_height_m,
                    dist_km=dist,
                    TSiteCriteria=0,
                    RSiteCriteria=0,
                    eps_dielect=DEFAULT_EPS_DIELECT,
                    sgm_conductivity=DEFAULT_GROUND,
                    eno_ns_surfref=301,
                    frq_mhz=freq_mhz,
                    radio_climate=DEFAULT_CLIMATE,
                    pol=1,
                    pctTime=reliability,
                    pctLoc=0.5,
                    pctConf=0.5,
                )
            except itm.InputError:
                dist += step_km
                continue

            rx_dbm = tx_dbm - loss_db
            if rx_dbm >= threshold_dbm:
                last_point = destination_point(lat, lon, bearing, dist)
                last_rx_dbm = rx_dbm
            dist += step_km

        if last_point and last_rx_dbm is not None:
            perimeter.append(last_point)

    return perimeter
