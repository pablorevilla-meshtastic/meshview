from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ADS1X15: TelemetrySensorType
ADS1X15_ALT: TelemetrySensorType
AHT10: TelemetrySensorType
AS3935: TelemetrySensorType
BH1750: TelemetrySensorType
BME280: TelemetrySensorType
BME680: TelemetrySensorType
BMP085: TelemetrySensorType
BMP280: TelemetrySensorType
BMP3XX: TelemetrySensorType
CUSTOM_SENSOR: TelemetrySensorType
DESCRIPTOR: _descriptor.FileDescriptor
DFROBOT_LARK: TelemetrySensorType
DFROBOT_RAIN: TelemetrySensorType
DPS310: TelemetrySensorType
DS248X: TelemetrySensorType
HDC1080: TelemetrySensorType
HM330X: TelemetrySensorType
ICM20948: TelemetrySensorType
ICM42607P: TelemetrySensorType
INA219: TelemetrySensorType
INA226: TelemetrySensorType
INA260: TelemetrySensorType
INA3221: TelemetrySensorType
LPS22: TelemetrySensorType
LTR390UV: TelemetrySensorType
MAX17048: TelemetrySensorType
MAX17261: TelemetrySensorType
MAX30102: TelemetrySensorType
MCP9808: TelemetrySensorType
MLX90614: TelemetrySensorType
MLX90632: TelemetrySensorType
MMC5983MA: TelemetrySensorType
NAU7802: TelemetrySensorType
OPT3001: TelemetrySensorType
PCT2075: TelemetrySensorType
PMSA003I: TelemetrySensorType
QMC5883L: TelemetrySensorType
QMC6310: TelemetrySensorType
QMI8658: TelemetrySensorType
RADSENS: TelemetrySensorType
RAK12035: TelemetrySensorType
RCWL9620: TelemetrySensorType
SCD30: TelemetrySensorType
SCD4X: TelemetrySensorType
SEN5X: TelemetrySensorType
SEN6X: TelemetrySensorType
SENSOR_UNSET: TelemetrySensorType
SFA30: TelemetrySensorType
SHT21: TelemetrySensorType
SHT31: TelemetrySensorType
SHT4X: TelemetrySensorType
SHTC3: TelemetrySensorType
SHTXX: TelemetrySensorType
SPA06: TelemetrySensorType
STC31: TelemetrySensorType
TSL2561: TelemetrySensorType
TSL25911FN: TelemetrySensorType
VEML7700: TelemetrySensorType

class AS3935State(_message.Message):
    __slots__ = ["tuning_cap_pf"]
    TUNING_CAP_PF_FIELD_NUMBER: _ClassVar[int]
    tuning_cap_pf: int
    def __init__(self, tuning_cap_pf: _Optional[int] = ...) -> None: ...

class AirQualityMetrics(_message.Message):
    __slots__ = ["co2", "co2_humidity", "co2_temperature", "form_formaldehyde", "form_humidity", "form_temperature", "particles_03um", "particles_05um", "particles_100um", "particles_10um", "particles_25um", "particles_40um", "particles_50um", "particles_tps", "pm100_environmental", "pm100_standard", "pm10_environmental", "pm10_standard", "pm25_environmental", "pm25_standard", "pm40_standard", "pm_humidity", "pm_nox_idx", "pm_status_flags", "pm_temperature", "pm_voc_idx"]
    CO2_FIELD_NUMBER: _ClassVar[int]
    CO2_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    CO2_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    FORM_FORMALDEHYDE_FIELD_NUMBER: _ClassVar[int]
    FORM_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    FORM_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_03UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_05UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_100UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_10UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_25UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_40UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_50UM_FIELD_NUMBER: _ClassVar[int]
    PARTICLES_TPS_FIELD_NUMBER: _ClassVar[int]
    PM100_ENVIRONMENTAL_FIELD_NUMBER: _ClassVar[int]
    PM100_STANDARD_FIELD_NUMBER: _ClassVar[int]
    PM10_ENVIRONMENTAL_FIELD_NUMBER: _ClassVar[int]
    PM10_STANDARD_FIELD_NUMBER: _ClassVar[int]
    PM25_ENVIRONMENTAL_FIELD_NUMBER: _ClassVar[int]
    PM25_STANDARD_FIELD_NUMBER: _ClassVar[int]
    PM40_STANDARD_FIELD_NUMBER: _ClassVar[int]
    PM_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    PM_NOX_IDX_FIELD_NUMBER: _ClassVar[int]
    PM_STATUS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PM_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    PM_VOC_IDX_FIELD_NUMBER: _ClassVar[int]
    co2: int
    co2_humidity: float
    co2_temperature: float
    form_formaldehyde: float
    form_humidity: float
    form_temperature: float
    particles_03um: int
    particles_05um: int
    particles_100um: int
    particles_10um: int
    particles_25um: int
    particles_40um: int
    particles_50um: int
    particles_tps: float
    pm100_environmental: int
    pm100_standard: int
    pm10_environmental: int
    pm10_standard: int
    pm25_environmental: int
    pm25_standard: int
    pm40_standard: int
    pm_humidity: float
    pm_nox_idx: float
    pm_status_flags: int
    pm_temperature: float
    pm_voc_idx: float
    def __init__(self, pm10_standard: _Optional[int] = ..., pm25_standard: _Optional[int] = ..., pm100_standard: _Optional[int] = ..., pm10_environmental: _Optional[int] = ..., pm25_environmental: _Optional[int] = ..., pm100_environmental: _Optional[int] = ..., particles_03um: _Optional[int] = ..., particles_05um: _Optional[int] = ..., particles_10um: _Optional[int] = ..., particles_25um: _Optional[int] = ..., particles_50um: _Optional[int] = ..., particles_100um: _Optional[int] = ..., co2: _Optional[int] = ..., co2_temperature: _Optional[float] = ..., co2_humidity: _Optional[float] = ..., form_formaldehyde: _Optional[float] = ..., form_humidity: _Optional[float] = ..., form_temperature: _Optional[float] = ..., pm40_standard: _Optional[int] = ..., particles_40um: _Optional[int] = ..., pm_temperature: _Optional[float] = ..., pm_humidity: _Optional[float] = ..., pm_voc_idx: _Optional[float] = ..., pm_nox_idx: _Optional[float] = ..., particles_tps: _Optional[float] = ..., pm_status_flags: _Optional[int] = ...) -> None: ...

class DeviceMetrics(_message.Message):
    __slots__ = ["air_util_tx", "battery_level", "channel_utilization", "uptime_seconds", "voltage"]
    AIR_UTIL_TX_FIELD_NUMBER: _ClassVar[int]
    BATTERY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    UPTIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    air_util_tx: float
    battery_level: int
    channel_utilization: float
    uptime_seconds: int
    voltage: float
    def __init__(self, battery_level: _Optional[int] = ..., voltage: _Optional[float] = ..., channel_utilization: _Optional[float] = ..., air_util_tx: _Optional[float] = ..., uptime_seconds: _Optional[int] = ...) -> None: ...

class EnvironmentMetrics(_message.Message):
    __slots__ = ["adc_voltage_ch0", "adc_voltage_ch1", "adc_voltage_ch2", "adc_voltage_ch3", "adc_voltage_ch4", "adc_voltage_ch5", "adc_voltage_ch6", "adc_voltage_ch7", "barometric_pressure", "current", "distance", "gas_resistance", "iaq", "ir_lux", "lightning_distance_km", "lightning_strike_count_1h", "lux", "one_wire_temperature", "one_wire_temperature_ch0", "one_wire_temperature_ch1", "one_wire_temperature_ch2", "one_wire_temperature_ch3", "one_wire_temperature_ch4", "one_wire_temperature_ch5", "one_wire_temperature_ch6", "one_wire_temperature_ch7", "radiation", "rainfall_1h", "rainfall_24h", "relative_humidity", "soil_moisture", "soil_temperature", "temperature", "uv_lux", "voltage", "weight", "white_lux", "wind_direction", "wind_gust", "wind_lull", "wind_speed"]
    ADC_VOLTAGE_CH0_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH1_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH2_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH3_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH4_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH5_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH6_FIELD_NUMBER: _ClassVar[int]
    ADC_VOLTAGE_CH7_FIELD_NUMBER: _ClassVar[int]
    BAROMETRIC_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    GAS_RESISTANCE_FIELD_NUMBER: _ClassVar[int]
    IAQ_FIELD_NUMBER: _ClassVar[int]
    IR_LUX_FIELD_NUMBER: _ClassVar[int]
    LIGHTNING_DISTANCE_KM_FIELD_NUMBER: _ClassVar[int]
    LIGHTNING_STRIKE_COUNT_1H_FIELD_NUMBER: _ClassVar[int]
    LUX_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH0_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH1_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH2_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH3_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH4_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH5_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH6_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_CH7_FIELD_NUMBER: _ClassVar[int]
    ONE_WIRE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    RADIATION_FIELD_NUMBER: _ClassVar[int]
    RAINFALL_1H_FIELD_NUMBER: _ClassVar[int]
    RAINFALL_24H_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    SOIL_MOISTURE_FIELD_NUMBER: _ClassVar[int]
    SOIL_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    UV_LUX_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    WHITE_LUX_FIELD_NUMBER: _ClassVar[int]
    WIND_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    WIND_GUST_FIELD_NUMBER: _ClassVar[int]
    WIND_LULL_FIELD_NUMBER: _ClassVar[int]
    WIND_SPEED_FIELD_NUMBER: _ClassVar[int]
    adc_voltage_ch0: float
    adc_voltage_ch1: float
    adc_voltage_ch2: float
    adc_voltage_ch3: float
    adc_voltage_ch4: float
    adc_voltage_ch5: float
    adc_voltage_ch6: float
    adc_voltage_ch7: float
    barometric_pressure: float
    current: float
    distance: float
    gas_resistance: float
    iaq: int
    ir_lux: float
    lightning_distance_km: float
    lightning_strike_count_1h: int
    lux: float
    one_wire_temperature: _containers.RepeatedScalarFieldContainer[float]
    one_wire_temperature_ch0: float
    one_wire_temperature_ch1: float
    one_wire_temperature_ch2: float
    one_wire_temperature_ch3: float
    one_wire_temperature_ch4: float
    one_wire_temperature_ch5: float
    one_wire_temperature_ch6: float
    one_wire_temperature_ch7: float
    radiation: float
    rainfall_1h: float
    rainfall_24h: float
    relative_humidity: float
    soil_moisture: int
    soil_temperature: float
    temperature: float
    uv_lux: float
    voltage: float
    weight: float
    white_lux: float
    wind_direction: int
    wind_gust: float
    wind_lull: float
    wind_speed: float
    def __init__(self, temperature: _Optional[float] = ..., relative_humidity: _Optional[float] = ..., barometric_pressure: _Optional[float] = ..., gas_resistance: _Optional[float] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., iaq: _Optional[int] = ..., distance: _Optional[float] = ..., lux: _Optional[float] = ..., white_lux: _Optional[float] = ..., ir_lux: _Optional[float] = ..., uv_lux: _Optional[float] = ..., wind_direction: _Optional[int] = ..., wind_speed: _Optional[float] = ..., weight: _Optional[float] = ..., wind_gust: _Optional[float] = ..., wind_lull: _Optional[float] = ..., radiation: _Optional[float] = ..., rainfall_1h: _Optional[float] = ..., rainfall_24h: _Optional[float] = ..., soil_moisture: _Optional[int] = ..., soil_temperature: _Optional[float] = ..., one_wire_temperature: _Optional[_Iterable[float]] = ..., adc_voltage_ch0: _Optional[float] = ..., adc_voltage_ch1: _Optional[float] = ..., adc_voltage_ch2: _Optional[float] = ..., adc_voltage_ch3: _Optional[float] = ..., adc_voltage_ch4: _Optional[float] = ..., adc_voltage_ch5: _Optional[float] = ..., adc_voltage_ch6: _Optional[float] = ..., adc_voltage_ch7: _Optional[float] = ..., one_wire_temperature_ch0: _Optional[float] = ..., one_wire_temperature_ch1: _Optional[float] = ..., one_wire_temperature_ch2: _Optional[float] = ..., one_wire_temperature_ch3: _Optional[float] = ..., one_wire_temperature_ch4: _Optional[float] = ..., one_wire_temperature_ch5: _Optional[float] = ..., one_wire_temperature_ch6: _Optional[float] = ..., one_wire_temperature_ch7: _Optional[float] = ..., lightning_strike_count_1h: _Optional[int] = ..., lightning_distance_km: _Optional[float] = ...) -> None: ...

class HealthMetrics(_message.Message):
    __slots__ = ["heart_bpm", "spO2", "temperature"]
    HEART_BPM_FIELD_NUMBER: _ClassVar[int]
    SPO2_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    heart_bpm: int
    spO2: int
    temperature: float
    def __init__(self, heart_bpm: _Optional[int] = ..., spO2: _Optional[int] = ..., temperature: _Optional[float] = ...) -> None: ...

class HostMetrics(_message.Message):
    __slots__ = ["diskfree1_bytes", "diskfree2_bytes", "diskfree3_bytes", "freemem_bytes", "load1", "load15", "load5", "uptime_seconds", "user_string"]
    DISKFREE1_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISKFREE2_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISKFREE3_BYTES_FIELD_NUMBER: _ClassVar[int]
    FREEMEM_BYTES_FIELD_NUMBER: _ClassVar[int]
    LOAD15_FIELD_NUMBER: _ClassVar[int]
    LOAD1_FIELD_NUMBER: _ClassVar[int]
    LOAD5_FIELD_NUMBER: _ClassVar[int]
    UPTIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    USER_STRING_FIELD_NUMBER: _ClassVar[int]
    diskfree1_bytes: int
    diskfree2_bytes: int
    diskfree3_bytes: int
    freemem_bytes: int
    load1: int
    load15: int
    load5: int
    uptime_seconds: int
    user_string: str
    def __init__(self, uptime_seconds: _Optional[int] = ..., freemem_bytes: _Optional[int] = ..., diskfree1_bytes: _Optional[int] = ..., diskfree2_bytes: _Optional[int] = ..., diskfree3_bytes: _Optional[int] = ..., load1: _Optional[int] = ..., load5: _Optional[int] = ..., load15: _Optional[int] = ..., user_string: _Optional[str] = ...) -> None: ...

class LocalStats(_message.Message):
    __slots__ = ["air_util_tx", "channel_utilization", "heap_free_bytes", "heap_total_bytes", "noise_floor", "num_online_nodes", "num_packets_rx", "num_packets_rx_bad", "num_packets_tx", "num_rx_dupe", "num_total_nodes", "num_tx_dropped", "num_tx_relay", "num_tx_relay_canceled", "uptime_seconds"]
    AIR_UTIL_TX_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    HEAP_FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
    HEAP_TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    NOISE_FLOOR_FIELD_NUMBER: _ClassVar[int]
    NUM_ONLINE_NODES_FIELD_NUMBER: _ClassVar[int]
    NUM_PACKETS_RX_BAD_FIELD_NUMBER: _ClassVar[int]
    NUM_PACKETS_RX_FIELD_NUMBER: _ClassVar[int]
    NUM_PACKETS_TX_FIELD_NUMBER: _ClassVar[int]
    NUM_RX_DUPE_FIELD_NUMBER: _ClassVar[int]
    NUM_TOTAL_NODES_FIELD_NUMBER: _ClassVar[int]
    NUM_TX_DROPPED_FIELD_NUMBER: _ClassVar[int]
    NUM_TX_RELAY_CANCELED_FIELD_NUMBER: _ClassVar[int]
    NUM_TX_RELAY_FIELD_NUMBER: _ClassVar[int]
    UPTIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    air_util_tx: float
    channel_utilization: float
    heap_free_bytes: int
    heap_total_bytes: int
    noise_floor: int
    num_online_nodes: int
    num_packets_rx: int
    num_packets_rx_bad: int
    num_packets_tx: int
    num_rx_dupe: int
    num_total_nodes: int
    num_tx_dropped: int
    num_tx_relay: int
    num_tx_relay_canceled: int
    uptime_seconds: int
    def __init__(self, uptime_seconds: _Optional[int] = ..., channel_utilization: _Optional[float] = ..., air_util_tx: _Optional[float] = ..., num_packets_tx: _Optional[int] = ..., num_packets_rx: _Optional[int] = ..., num_packets_rx_bad: _Optional[int] = ..., num_online_nodes: _Optional[int] = ..., num_total_nodes: _Optional[int] = ..., num_rx_dupe: _Optional[int] = ..., num_tx_relay: _Optional[int] = ..., num_tx_relay_canceled: _Optional[int] = ..., heap_total_bytes: _Optional[int] = ..., heap_free_bytes: _Optional[int] = ..., num_tx_dropped: _Optional[int] = ..., noise_floor: _Optional[int] = ...) -> None: ...

class Nau7802Config(_message.Message):
    __slots__ = ["calibrationFactor", "zeroOffset"]
    CALIBRATIONFACTOR_FIELD_NUMBER: _ClassVar[int]
    ZEROOFFSET_FIELD_NUMBER: _ClassVar[int]
    calibrationFactor: float
    zeroOffset: int
    def __init__(self, zeroOffset: _Optional[int] = ..., calibrationFactor: _Optional[float] = ...) -> None: ...

class PowerMetrics(_message.Message):
    __slots__ = ["ch1_current", "ch1_voltage", "ch2_current", "ch2_voltage", "ch3_current", "ch3_voltage", "ch4_current", "ch4_voltage", "ch5_current", "ch5_voltage", "ch6_current", "ch6_voltage", "ch7_current", "ch7_voltage", "ch8_current", "ch8_voltage"]
    CH1_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH1_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH2_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH2_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH3_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH3_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH4_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH4_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH5_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH5_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH6_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH6_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH7_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH7_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CH8_CURRENT_FIELD_NUMBER: _ClassVar[int]
    CH8_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    ch1_current: float
    ch1_voltage: float
    ch2_current: float
    ch2_voltage: float
    ch3_current: float
    ch3_voltage: float
    ch4_current: float
    ch4_voltage: float
    ch5_current: float
    ch5_voltage: float
    ch6_current: float
    ch6_voltage: float
    ch7_current: float
    ch7_voltage: float
    ch8_current: float
    ch8_voltage: float
    def __init__(self, ch1_voltage: _Optional[float] = ..., ch1_current: _Optional[float] = ..., ch2_voltage: _Optional[float] = ..., ch2_current: _Optional[float] = ..., ch3_voltage: _Optional[float] = ..., ch3_current: _Optional[float] = ..., ch4_voltage: _Optional[float] = ..., ch4_current: _Optional[float] = ..., ch5_voltage: _Optional[float] = ..., ch5_current: _Optional[float] = ..., ch6_voltage: _Optional[float] = ..., ch6_current: _Optional[float] = ..., ch7_voltage: _Optional[float] = ..., ch7_current: _Optional[float] = ..., ch8_voltage: _Optional[float] = ..., ch8_current: _Optional[float] = ...) -> None: ...

class SEN5XState(_message.Message):
    __slots__ = ["last_cleaning_time", "last_cleaning_valid", "one_shot_mode", "voc_state_array", "voc_state_time", "voc_state_valid"]
    LAST_CLEANING_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_CLEANING_VALID_FIELD_NUMBER: _ClassVar[int]
    ONE_SHOT_MODE_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_ARRAY_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_TIME_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_VALID_FIELD_NUMBER: _ClassVar[int]
    last_cleaning_time: int
    last_cleaning_valid: bool
    one_shot_mode: bool
    voc_state_array: int
    voc_state_time: int
    voc_state_valid: bool
    def __init__(self, last_cleaning_time: _Optional[int] = ..., last_cleaning_valid: bool = ..., one_shot_mode: bool = ..., voc_state_time: _Optional[int] = ..., voc_state_valid: bool = ..., voc_state_array: _Optional[int] = ...) -> None: ...

class SEN6XState(_message.Message):
    __slots__ = ["last_cleaning_time", "last_cleaning_valid", "one_shot_mode", "voc_state_array", "voc_state_time", "voc_state_valid"]
    LAST_CLEANING_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_CLEANING_VALID_FIELD_NUMBER: _ClassVar[int]
    ONE_SHOT_MODE_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_ARRAY_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_TIME_FIELD_NUMBER: _ClassVar[int]
    VOC_STATE_VALID_FIELD_NUMBER: _ClassVar[int]
    last_cleaning_time: int
    last_cleaning_valid: bool
    one_shot_mode: bool
    voc_state_array: int
    voc_state_time: int
    voc_state_valid: bool
    def __init__(self, last_cleaning_time: _Optional[int] = ..., last_cleaning_valid: bool = ..., one_shot_mode: bool = ..., voc_state_time: _Optional[int] = ..., voc_state_valid: bool = ..., voc_state_array: _Optional[int] = ...) -> None: ...

class SoilWaterMetrics(_message.Message):
    __slots__ = ["ammonium", "biochemical_oxygen_demand", "chemical_oxygen_demand", "dissolved_oxygen", "electrical_conductivity", "nitrate", "nitrogen", "orp", "ph", "phosphorus", "potassium", "salinity", "soil_ph", "solar_irradiance", "turbidity"]
    AMMONIUM_FIELD_NUMBER: _ClassVar[int]
    BIOCHEMICAL_OXYGEN_DEMAND_FIELD_NUMBER: _ClassVar[int]
    CHEMICAL_OXYGEN_DEMAND_FIELD_NUMBER: _ClassVar[int]
    DISSOLVED_OXYGEN_FIELD_NUMBER: _ClassVar[int]
    ELECTRICAL_CONDUCTIVITY_FIELD_NUMBER: _ClassVar[int]
    NITRATE_FIELD_NUMBER: _ClassVar[int]
    NITROGEN_FIELD_NUMBER: _ClassVar[int]
    ORP_FIELD_NUMBER: _ClassVar[int]
    PHOSPHORUS_FIELD_NUMBER: _ClassVar[int]
    PH_FIELD_NUMBER: _ClassVar[int]
    POTASSIUM_FIELD_NUMBER: _ClassVar[int]
    SALINITY_FIELD_NUMBER: _ClassVar[int]
    SOIL_PH_FIELD_NUMBER: _ClassVar[int]
    SOLAR_IRRADIANCE_FIELD_NUMBER: _ClassVar[int]
    TURBIDITY_FIELD_NUMBER: _ClassVar[int]
    ammonium: float
    biochemical_oxygen_demand: float
    chemical_oxygen_demand: float
    dissolved_oxygen: float
    electrical_conductivity: float
    nitrate: float
    nitrogen: float
    orp: float
    ph: float
    phosphorus: float
    potassium: float
    salinity: float
    soil_ph: float
    solar_irradiance: float
    turbidity: float
    def __init__(self, soil_ph: _Optional[float] = ..., ph: _Optional[float] = ..., electrical_conductivity: _Optional[float] = ..., salinity: _Optional[float] = ..., nitrogen: _Optional[float] = ..., phosphorus: _Optional[float] = ..., potassium: _Optional[float] = ..., dissolved_oxygen: _Optional[float] = ..., orp: _Optional[float] = ..., chemical_oxygen_demand: _Optional[float] = ..., turbidity: _Optional[float] = ..., nitrate: _Optional[float] = ..., ammonium: _Optional[float] = ..., biochemical_oxygen_demand: _Optional[float] = ..., solar_irradiance: _Optional[float] = ...) -> None: ...

class Telemetry(_message.Message):
    __slots__ = ["air_quality_metrics", "device_metrics", "environment_metrics", "health_metrics", "host_metrics", "local_stats", "power_metrics", "soil_water_metrics", "time", "traffic_management_stats"]
    AIR_QUALITY_METRICS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_METRICS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_METRICS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_METRICS_FIELD_NUMBER: _ClassVar[int]
    HOST_METRICS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_STATS_FIELD_NUMBER: _ClassVar[int]
    POWER_METRICS_FIELD_NUMBER: _ClassVar[int]
    SOIL_WATER_METRICS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_MANAGEMENT_STATS_FIELD_NUMBER: _ClassVar[int]
    air_quality_metrics: AirQualityMetrics
    device_metrics: DeviceMetrics
    environment_metrics: EnvironmentMetrics
    health_metrics: HealthMetrics
    host_metrics: HostMetrics
    local_stats: LocalStats
    power_metrics: PowerMetrics
    soil_water_metrics: SoilWaterMetrics
    time: int
    traffic_management_stats: TrafficManagementStats
    def __init__(self, time: _Optional[int] = ..., device_metrics: _Optional[_Union[DeviceMetrics, _Mapping]] = ..., environment_metrics: _Optional[_Union[EnvironmentMetrics, _Mapping]] = ..., air_quality_metrics: _Optional[_Union[AirQualityMetrics, _Mapping]] = ..., power_metrics: _Optional[_Union[PowerMetrics, _Mapping]] = ..., local_stats: _Optional[_Union[LocalStats, _Mapping]] = ..., health_metrics: _Optional[_Union[HealthMetrics, _Mapping]] = ..., host_metrics: _Optional[_Union[HostMetrics, _Mapping]] = ..., traffic_management_stats: _Optional[_Union[TrafficManagementStats, _Mapping]] = ..., soil_water_metrics: _Optional[_Union[SoilWaterMetrics, _Mapping]] = ...) -> None: ...

class TrafficManagementStats(_message.Message):
    __slots__ = ["hop_exhausted_packets", "nodeinfo_cache_hits", "packets_inspected", "position_dedup_drops", "rate_limit_drops", "router_hops_preserved", "unknown_packet_drops"]
    HOP_EXHAUSTED_PACKETS_FIELD_NUMBER: _ClassVar[int]
    NODEINFO_CACHE_HITS_FIELD_NUMBER: _ClassVar[int]
    PACKETS_INSPECTED_FIELD_NUMBER: _ClassVar[int]
    POSITION_DEDUP_DROPS_FIELD_NUMBER: _ClassVar[int]
    RATE_LIMIT_DROPS_FIELD_NUMBER: _ClassVar[int]
    ROUTER_HOPS_PRESERVED_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_PACKET_DROPS_FIELD_NUMBER: _ClassVar[int]
    hop_exhausted_packets: int
    nodeinfo_cache_hits: int
    packets_inspected: int
    position_dedup_drops: int
    rate_limit_drops: int
    router_hops_preserved: int
    unknown_packet_drops: int
    def __init__(self, packets_inspected: _Optional[int] = ..., position_dedup_drops: _Optional[int] = ..., nodeinfo_cache_hits: _Optional[int] = ..., rate_limit_drops: _Optional[int] = ..., unknown_packet_drops: _Optional[int] = ..., hop_exhausted_packets: _Optional[int] = ..., router_hops_preserved: _Optional[int] = ...) -> None: ...

class TelemetrySensorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
