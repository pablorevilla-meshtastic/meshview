from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

AZERBAIJANI: Language
BULGARIAN: Language
CZECH: Language
DANISH: Language
DARK: Theme
DESCRIPTOR: _descriptor.FileDescriptor
DUTCH: Language
DYNAMIC: CompassMode
ENGLISH: Language
FINNISH: Language
FIXED_RING: CompassMode
FREEZE_HEADING: CompassMode
FRENCH: Language
GERMAN: Language
GREEK: Language
HUNGARIAN: Language
ITALIAN: Language
LIGHT: Theme
NORWEGIAN: Language
POLISH: Language
PORTUGUESE: Language
RED: Theme
RUSSIAN: Language
SERBIAN: Language
SIMPLIFIED_CHINESE: Language
SLOVENIAN: Language
SPANISH: Language
SWEDISH: Language
TRADITIONAL_CHINESE: Language
TURKISH: Language
UKRAINIAN: Language

class DeviceUIConfig(_message.Message):
    __slots__ = ["alert_enabled", "banner_enabled", "calibration_data", "compass_mode", "gps_format", "is_clockface_analog", "language", "map_data", "node_filter", "node_highlight", "pin_code", "ring_tone_id", "screen_brightness", "screen_lock", "screen_rgb_color", "screen_timeout", "settings_lock", "theme", "version"]
    class GpsCoordinateFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ALERT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    BANNER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_DATA_FIELD_NUMBER: _ClassVar[int]
    COMPASS_MODE_FIELD_NUMBER: _ClassVar[int]
    DEC: DeviceUIConfig.GpsCoordinateFormat
    DMS: DeviceUIConfig.GpsCoordinateFormat
    GPS_FORMAT_FIELD_NUMBER: _ClassVar[int]
    IS_CLOCKFACE_ANALOG_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    MAP_DATA_FIELD_NUMBER: _ClassVar[int]
    MGRS: DeviceUIConfig.GpsCoordinateFormat
    MLS: DeviceUIConfig.GpsCoordinateFormat
    NODE_FILTER_FIELD_NUMBER: _ClassVar[int]
    NODE_HIGHLIGHT_FIELD_NUMBER: _ClassVar[int]
    OLC: DeviceUIConfig.GpsCoordinateFormat
    OSGR: DeviceUIConfig.GpsCoordinateFormat
    PIN_CODE_FIELD_NUMBER: _ClassVar[int]
    RING_TONE_ID_FIELD_NUMBER: _ClassVar[int]
    SCREEN_BRIGHTNESS_FIELD_NUMBER: _ClassVar[int]
    SCREEN_LOCK_FIELD_NUMBER: _ClassVar[int]
    SCREEN_RGB_COLOR_FIELD_NUMBER: _ClassVar[int]
    SCREEN_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_LOCK_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    UTM: DeviceUIConfig.GpsCoordinateFormat
    VERSION_FIELD_NUMBER: _ClassVar[int]
    alert_enabled: bool
    banner_enabled: bool
    calibration_data: bytes
    compass_mode: CompassMode
    gps_format: DeviceUIConfig.GpsCoordinateFormat
    is_clockface_analog: bool
    language: Language
    map_data: Map
    node_filter: NodeFilter
    node_highlight: NodeHighlight
    pin_code: int
    ring_tone_id: int
    screen_brightness: int
    screen_lock: bool
    screen_rgb_color: int
    screen_timeout: int
    settings_lock: bool
    theme: Theme
    version: int
    def __init__(self, version: _Optional[int] = ..., screen_brightness: _Optional[int] = ..., screen_timeout: _Optional[int] = ..., screen_lock: bool = ..., settings_lock: bool = ..., pin_code: _Optional[int] = ..., theme: _Optional[_Union[Theme, str]] = ..., alert_enabled: bool = ..., banner_enabled: bool = ..., ring_tone_id: _Optional[int] = ..., language: _Optional[_Union[Language, str]] = ..., node_filter: _Optional[_Union[NodeFilter, _Mapping]] = ..., node_highlight: _Optional[_Union[NodeHighlight, _Mapping]] = ..., calibration_data: _Optional[bytes] = ..., map_data: _Optional[_Union[Map, _Mapping]] = ..., compass_mode: _Optional[_Union[CompassMode, str]] = ..., screen_rgb_color: _Optional[int] = ..., is_clockface_analog: bool = ..., gps_format: _Optional[_Union[DeviceUIConfig.GpsCoordinateFormat, str]] = ...) -> None: ...

class GeoPoint(_message.Message):
    __slots__ = ["latitude", "longitude", "zoom"]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    latitude: int
    longitude: int
    zoom: int
    def __init__(self, zoom: _Optional[int] = ..., latitude: _Optional[int] = ..., longitude: _Optional[int] = ...) -> None: ...

class Map(_message.Message):
    __slots__ = ["follow_gps", "home", "style"]
    FOLLOW_GPS_FIELD_NUMBER: _ClassVar[int]
    HOME_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    follow_gps: bool
    home: GeoPoint
    style: str
    def __init__(self, home: _Optional[_Union[GeoPoint, _Mapping]] = ..., style: _Optional[str] = ..., follow_gps: bool = ...) -> None: ...

class NodeFilter(_message.Message):
    __slots__ = ["channel", "hops_away", "node_name", "offline_switch", "position_switch", "public_key_switch", "unknown_switch"]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    HOPS_AWAY_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_SWITCH_FIELD_NUMBER: _ClassVar[int]
    POSITION_SWITCH_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_SWITCH_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_SWITCH_FIELD_NUMBER: _ClassVar[int]
    channel: int
    hops_away: int
    node_name: str
    offline_switch: bool
    position_switch: bool
    public_key_switch: bool
    unknown_switch: bool
    def __init__(self, unknown_switch: bool = ..., offline_switch: bool = ..., public_key_switch: bool = ..., hops_away: _Optional[int] = ..., position_switch: bool = ..., node_name: _Optional[str] = ..., channel: _Optional[int] = ...) -> None: ...

class NodeHighlight(_message.Message):
    __slots__ = ["chat_switch", "iaq_switch", "node_name", "position_switch", "telemetry_switch"]
    CHAT_SWITCH_FIELD_NUMBER: _ClassVar[int]
    IAQ_SWITCH_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_SWITCH_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_SWITCH_FIELD_NUMBER: _ClassVar[int]
    chat_switch: bool
    iaq_switch: bool
    node_name: str
    position_switch: bool
    telemetry_switch: bool
    def __init__(self, chat_switch: bool = ..., position_switch: bool = ..., telemetry_switch: bool = ..., iaq_switch: bool = ..., node_name: _Optional[str] = ...) -> None: ...

class CompassMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Theme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Language(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
