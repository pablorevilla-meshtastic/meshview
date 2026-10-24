from meshtastic.protobuf import device_ui_pb2 as _device_ui_pb2
from meshtastic.protobuf import field_metadata_pb2 as _field_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ["bluetooth", "device", "device_ui", "display", "lora", "network", "position", "power", "security", "sessionkey"]
    class BluetoothConfig(_message.Message):
        __slots__ = ["enabled", "fixed_pin", "mode"]
        class PairingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        FIXED_PIN: Config.BluetoothConfig.PairingMode
        FIXED_PIN_FIELD_NUMBER: _ClassVar[int]
        MODE_FIELD_NUMBER: _ClassVar[int]
        NO_PIN: Config.BluetoothConfig.PairingMode
        RANDOM_PIN: Config.BluetoothConfig.PairingMode
        enabled: bool
        fixed_pin: int
        mode: Config.BluetoothConfig.PairingMode
        def __init__(self, enabled: bool = ..., mode: _Optional[_Union[Config.BluetoothConfig.PairingMode, str]] = ..., fixed_pin: _Optional[int] = ...) -> None: ...
    class DeviceConfig(_message.Message):
        __slots__ = ["button_gpio", "buzzer_gpio", "buzzer_mode", "disable_triple_click", "double_tap_as_button_press", "is_managed", "led_heartbeat_disabled", "node_info_broadcast_secs", "rebroadcast_mode", "role", "serial_enabled", "tzdef"]
        class BuzzerMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class RebroadcastMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ALL: Config.DeviceConfig.RebroadcastMode
        ALL_ENABLED: Config.DeviceConfig.BuzzerMode
        ALL_SKIP_DECODING: Config.DeviceConfig.RebroadcastMode
        BUTTON_GPIO_FIELD_NUMBER: _ClassVar[int]
        BUZZER_GPIO_FIELD_NUMBER: _ClassVar[int]
        BUZZER_MODE_FIELD_NUMBER: _ClassVar[int]
        CLIENT: Config.DeviceConfig.Role
        CLIENT_BASE: Config.DeviceConfig.Role
        CLIENT_HIDDEN: Config.DeviceConfig.Role
        CLIENT_MUTE: Config.DeviceConfig.Role
        CORE_PORTNUMS_ONLY: Config.DeviceConfig.RebroadcastMode
        DIRECT_MSG_ONLY: Config.DeviceConfig.BuzzerMode
        DISABLED: Config.DeviceConfig.BuzzerMode
        DISABLE_TRIPLE_CLICK_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_TAP_AS_BUTTON_PRESS_FIELD_NUMBER: _ClassVar[int]
        IS_MANAGED_FIELD_NUMBER: _ClassVar[int]
        KNOWN_ONLY: Config.DeviceConfig.RebroadcastMode
        LED_HEARTBEAT_DISABLED_FIELD_NUMBER: _ClassVar[int]
        LOCAL_ONLY: Config.DeviceConfig.RebroadcastMode
        LOST_AND_FOUND: Config.DeviceConfig.Role
        NODE_INFO_BROADCAST_SECS_FIELD_NUMBER: _ClassVar[int]
        NONE: Config.DeviceConfig.RebroadcastMode
        NOTIFICATIONS_ONLY: Config.DeviceConfig.BuzzerMode
        REBROADCAST_MODE_FIELD_NUMBER: _ClassVar[int]
        REPEATER: Config.DeviceConfig.Role
        ROLE_FIELD_NUMBER: _ClassVar[int]
        ROUTER: Config.DeviceConfig.Role
        ROUTER_CLIENT: Config.DeviceConfig.Role
        ROUTER_LATE: Config.DeviceConfig.Role
        SENSOR: Config.DeviceConfig.Role
        SERIAL_ENABLED_FIELD_NUMBER: _ClassVar[int]
        SYSTEM_ONLY: Config.DeviceConfig.BuzzerMode
        TAK: Config.DeviceConfig.Role
        TAK_TRACKER: Config.DeviceConfig.Role
        TRACKER: Config.DeviceConfig.Role
        TZDEF_FIELD_NUMBER: _ClassVar[int]
        button_gpio: int
        buzzer_gpio: int
        buzzer_mode: Config.DeviceConfig.BuzzerMode
        disable_triple_click: bool
        double_tap_as_button_press: bool
        is_managed: bool
        led_heartbeat_disabled: bool
        node_info_broadcast_secs: int
        rebroadcast_mode: Config.DeviceConfig.RebroadcastMode
        role: Config.DeviceConfig.Role
        serial_enabled: bool
        tzdef: str
        def __init__(self, role: _Optional[_Union[Config.DeviceConfig.Role, str]] = ..., serial_enabled: bool = ..., button_gpio: _Optional[int] = ..., buzzer_gpio: _Optional[int] = ..., rebroadcast_mode: _Optional[_Union[Config.DeviceConfig.RebroadcastMode, str]] = ..., node_info_broadcast_secs: _Optional[int] = ..., double_tap_as_button_press: bool = ..., is_managed: bool = ..., disable_triple_click: bool = ..., tzdef: _Optional[str] = ..., led_heartbeat_disabled: bool = ..., buzzer_mode: _Optional[_Union[Config.DeviceConfig.BuzzerMode, str]] = ...) -> None: ...
    class DisplayConfig(_message.Message):
        __slots__ = ["auto_screen_carousel_secs", "compass_north_top", "compass_orientation", "displaymode", "enable_message_bubbles", "flip_screen", "gps_format", "heading_bold", "oled", "screen_on_secs", "units", "use_12h_clock", "use_long_node_name", "wake_on_tap_or_motion"]
        class CompassOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class DeprecatedGpsCoordinateFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class DisplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class DisplayUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class OledType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        AUTO_SCREEN_CAROUSEL_SECS_FIELD_NUMBER: _ClassVar[int]
        COLOR: Config.DisplayConfig.DisplayMode
        COMPASS_NORTH_TOP_FIELD_NUMBER: _ClassVar[int]
        COMPASS_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
        DEFAULT: Config.DisplayConfig.DisplayMode
        DEGREES_0: Config.DisplayConfig.CompassOrientation
        DEGREES_0_INVERTED: Config.DisplayConfig.CompassOrientation
        DEGREES_180: Config.DisplayConfig.CompassOrientation
        DEGREES_180_INVERTED: Config.DisplayConfig.CompassOrientation
        DEGREES_270: Config.DisplayConfig.CompassOrientation
        DEGREES_270_INVERTED: Config.DisplayConfig.CompassOrientation
        DEGREES_90: Config.DisplayConfig.CompassOrientation
        DEGREES_90_INVERTED: Config.DisplayConfig.CompassOrientation
        DISPLAYMODE_FIELD_NUMBER: _ClassVar[int]
        ENABLE_MESSAGE_BUBBLES_FIELD_NUMBER: _ClassVar[int]
        FLIP_SCREEN_FIELD_NUMBER: _ClassVar[int]
        GPS_FORMAT_FIELD_NUMBER: _ClassVar[int]
        HEADING_BOLD_FIELD_NUMBER: _ClassVar[int]
        IMPERIAL: Config.DisplayConfig.DisplayUnits
        INVERTED: Config.DisplayConfig.DisplayMode
        METRIC: Config.DisplayConfig.DisplayUnits
        OLED_AUTO: Config.DisplayConfig.OledType
        OLED_FIELD_NUMBER: _ClassVar[int]
        OLED_SH1106: Config.DisplayConfig.OledType
        OLED_SH1107: Config.DisplayConfig.OledType
        OLED_SH1107_128_128: Config.DisplayConfig.OledType
        OLED_SH1107_ROTATED: Config.DisplayConfig.OledType
        OLED_SSD1306: Config.DisplayConfig.OledType
        SCREEN_ON_SECS_FIELD_NUMBER: _ClassVar[int]
        TWOCOLOR: Config.DisplayConfig.DisplayMode
        UNITS_FIELD_NUMBER: _ClassVar[int]
        UNUSED: Config.DisplayConfig.DeprecatedGpsCoordinateFormat
        USE_12H_CLOCK_FIELD_NUMBER: _ClassVar[int]
        USE_LONG_NODE_NAME_FIELD_NUMBER: _ClassVar[int]
        WAKE_ON_TAP_OR_MOTION_FIELD_NUMBER: _ClassVar[int]
        auto_screen_carousel_secs: int
        compass_north_top: bool
        compass_orientation: Config.DisplayConfig.CompassOrientation
        displaymode: Config.DisplayConfig.DisplayMode
        enable_message_bubbles: bool
        flip_screen: bool
        gps_format: Config.DisplayConfig.DeprecatedGpsCoordinateFormat
        heading_bold: bool
        oled: Config.DisplayConfig.OledType
        screen_on_secs: int
        units: Config.DisplayConfig.DisplayUnits
        use_12h_clock: bool
        use_long_node_name: bool
        wake_on_tap_or_motion: bool
        def __init__(self, screen_on_secs: _Optional[int] = ..., gps_format: _Optional[_Union[Config.DisplayConfig.DeprecatedGpsCoordinateFormat, str]] = ..., auto_screen_carousel_secs: _Optional[int] = ..., compass_north_top: bool = ..., flip_screen: bool = ..., units: _Optional[_Union[Config.DisplayConfig.DisplayUnits, str]] = ..., oled: _Optional[_Union[Config.DisplayConfig.OledType, str]] = ..., displaymode: _Optional[_Union[Config.DisplayConfig.DisplayMode, str]] = ..., heading_bold: bool = ..., wake_on_tap_or_motion: bool = ..., compass_orientation: _Optional[_Union[Config.DisplayConfig.CompassOrientation, str]] = ..., use_12h_clock: bool = ..., use_long_node_name: bool = ..., enable_message_bubbles: bool = ...) -> None: ...
    class LoRaConfig(_message.Message):
        __slots__ = ["bandwidth", "channel_num", "coding_rate", "config_ok_to_mqtt", "fem_lna_mode", "frequency_offset", "hop_limit", "ignore_incoming", "ignore_mqtt", "modem_preset", "override_duty_cycle", "override_frequency", "pa_fan_disabled", "region", "serial_hal_only", "spread_factor", "sx126x_rx_boosted_gain", "tx_enabled", "tx_power", "use_preset"]
        class FEM_LNA_Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class ModemPreset(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class RegionCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ANZ: Config.LoRaConfig.RegionCode
        ANZ_433: Config.LoRaConfig.RegionCode
        BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
        BR_902: Config.LoRaConfig.RegionCode
        CHANNEL_NUM_FIELD_NUMBER: _ClassVar[int]
        CN: Config.LoRaConfig.RegionCode
        CODING_RATE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_OK_TO_MQTT_FIELD_NUMBER: _ClassVar[int]
        DISABLED: Config.LoRaConfig.FEM_LNA_Mode
        ENABLED: Config.LoRaConfig.FEM_LNA_Mode
        EU_433: Config.LoRaConfig.RegionCode
        EU_866: Config.LoRaConfig.RegionCode
        EU_868: Config.LoRaConfig.RegionCode
        EU_874: Config.LoRaConfig.RegionCode
        EU_917: Config.LoRaConfig.RegionCode
        EU_N_868: Config.LoRaConfig.RegionCode
        FEM_LNA_MODE_FIELD_NUMBER: _ClassVar[int]
        FREQUENCY_OFFSET_FIELD_NUMBER: _ClassVar[int]
        HOP_LIMIT_FIELD_NUMBER: _ClassVar[int]
        IGNORE_INCOMING_FIELD_NUMBER: _ClassVar[int]
        IGNORE_MQTT_FIELD_NUMBER: _ClassVar[int]
        IN: Config.LoRaConfig.RegionCode
        ITU1_2M: Config.LoRaConfig.RegionCode
        ITU1_70CM: Config.LoRaConfig.RegionCode
        ITU2_125CM: Config.LoRaConfig.RegionCode
        ITU2_2M: Config.LoRaConfig.RegionCode
        ITU2_70CM: Config.LoRaConfig.RegionCode
        ITU3_2M: Config.LoRaConfig.RegionCode
        ITU3_70CM: Config.LoRaConfig.RegionCode
        JP: Config.LoRaConfig.RegionCode
        KR: Config.LoRaConfig.RegionCode
        KZ_433: Config.LoRaConfig.RegionCode
        KZ_863: Config.LoRaConfig.RegionCode
        LITE_FAST: Config.LoRaConfig.ModemPreset
        LITE_SLOW: Config.LoRaConfig.ModemPreset
        LONG_FAST: Config.LoRaConfig.ModemPreset
        LONG_MODERATE: Config.LoRaConfig.ModemPreset
        LONG_SLOW: Config.LoRaConfig.ModemPreset
        LONG_TURBO: Config.LoRaConfig.ModemPreset
        LORA_24: Config.LoRaConfig.RegionCode
        MEDIUM_FAST: Config.LoRaConfig.ModemPreset
        MEDIUM_SLOW: Config.LoRaConfig.ModemPreset
        MEDIUM_TURBO: Config.LoRaConfig.ModemPreset
        MODEM_PRESET_FIELD_NUMBER: _ClassVar[int]
        MY_433: Config.LoRaConfig.RegionCode
        MY_919: Config.LoRaConfig.RegionCode
        NARROW_FAST: Config.LoRaConfig.ModemPreset
        NARROW_SLOW: Config.LoRaConfig.ModemPreset
        NOT_PRESENT: Config.LoRaConfig.FEM_LNA_Mode
        NP_865: Config.LoRaConfig.RegionCode
        NZ_865: Config.LoRaConfig.RegionCode
        OVERRIDE_DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
        OVERRIDE_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        PA_FAN_DISABLED_FIELD_NUMBER: _ClassVar[int]
        PH_433: Config.LoRaConfig.RegionCode
        PH_868: Config.LoRaConfig.RegionCode
        PH_915: Config.LoRaConfig.RegionCode
        REGION_FIELD_NUMBER: _ClassVar[int]
        RU: Config.LoRaConfig.RegionCode
        SERIAL_HAL_ONLY_FIELD_NUMBER: _ClassVar[int]
        SG_923: Config.LoRaConfig.RegionCode
        SHORT_FAST: Config.LoRaConfig.ModemPreset
        SHORT_SLOW: Config.LoRaConfig.ModemPreset
        SHORT_TURBO: Config.LoRaConfig.ModemPreset
        SPREAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
        SX126X_RX_BOOSTED_GAIN_FIELD_NUMBER: _ClassVar[int]
        TH: Config.LoRaConfig.RegionCode
        TINY_FAST: Config.LoRaConfig.ModemPreset
        TINY_SLOW: Config.LoRaConfig.ModemPreset
        TW: Config.LoRaConfig.RegionCode
        TX_ENABLED_FIELD_NUMBER: _ClassVar[int]
        TX_POWER_FIELD_NUMBER: _ClassVar[int]
        UA_433: Config.LoRaConfig.RegionCode
        UA_868: Config.LoRaConfig.RegionCode
        UNSET: Config.LoRaConfig.RegionCode
        US: Config.LoRaConfig.RegionCode
        USE_PRESET_FIELD_NUMBER: _ClassVar[int]
        VERY_LONG_SLOW: Config.LoRaConfig.ModemPreset
        bandwidth: int
        channel_num: int
        coding_rate: int
        config_ok_to_mqtt: bool
        fem_lna_mode: Config.LoRaConfig.FEM_LNA_Mode
        frequency_offset: float
        hop_limit: int
        ignore_incoming: _containers.RepeatedScalarFieldContainer[int]
        ignore_mqtt: bool
        modem_preset: Config.LoRaConfig.ModemPreset
        override_duty_cycle: bool
        override_frequency: float
        pa_fan_disabled: bool
        region: Config.LoRaConfig.RegionCode
        serial_hal_only: bool
        spread_factor: int
        sx126x_rx_boosted_gain: bool
        tx_enabled: bool
        tx_power: int
        use_preset: bool
        def __init__(self, use_preset: bool = ..., modem_preset: _Optional[_Union[Config.LoRaConfig.ModemPreset, str]] = ..., bandwidth: _Optional[int] = ..., spread_factor: _Optional[int] = ..., coding_rate: _Optional[int] = ..., frequency_offset: _Optional[float] = ..., region: _Optional[_Union[Config.LoRaConfig.RegionCode, str]] = ..., hop_limit: _Optional[int] = ..., tx_enabled: bool = ..., tx_power: _Optional[int] = ..., channel_num: _Optional[int] = ..., override_duty_cycle: bool = ..., sx126x_rx_boosted_gain: bool = ..., override_frequency: _Optional[float] = ..., pa_fan_disabled: bool = ..., ignore_incoming: _Optional[_Iterable[int]] = ..., ignore_mqtt: bool = ..., config_ok_to_mqtt: bool = ..., fem_lna_mode: _Optional[_Union[Config.LoRaConfig.FEM_LNA_Mode, str]] = ..., serial_hal_only: bool = ...) -> None: ...
    class NetworkConfig(_message.Message):
        __slots__ = ["address_mode", "enabled_protocols", "eth_enabled", "ipv4_config", "ipv6_enabled", "ntp_server", "rsyslog_server", "wifi_enabled", "wifi_psk", "wifi_ssid"]
        class AddressMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class ProtocolFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class IpV4Config(_message.Message):
            __slots__ = ["dns", "gateway", "ip", "subnet"]
            DNS_FIELD_NUMBER: _ClassVar[int]
            GATEWAY_FIELD_NUMBER: _ClassVar[int]
            IP_FIELD_NUMBER: _ClassVar[int]
            SUBNET_FIELD_NUMBER: _ClassVar[int]
            dns: int
            gateway: int
            ip: int
            subnet: int
            def __init__(self, ip: _Optional[int] = ..., gateway: _Optional[int] = ..., subnet: _Optional[int] = ..., dns: _Optional[int] = ...) -> None: ...
        ADDRESS_MODE_FIELD_NUMBER: _ClassVar[int]
        DHCP: Config.NetworkConfig.AddressMode
        ENABLED_PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
        ETH_ENABLED_FIELD_NUMBER: _ClassVar[int]
        IPV4_CONFIG_FIELD_NUMBER: _ClassVar[int]
        IPV6_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NO_BROADCAST: Config.NetworkConfig.ProtocolFlags
        NTP_SERVER_FIELD_NUMBER: _ClassVar[int]
        RSYSLOG_SERVER_FIELD_NUMBER: _ClassVar[int]
        STATIC: Config.NetworkConfig.AddressMode
        UDP_BROADCAST: Config.NetworkConfig.ProtocolFlags
        WIFI_ENABLED_FIELD_NUMBER: _ClassVar[int]
        WIFI_PSK_FIELD_NUMBER: _ClassVar[int]
        WIFI_SSID_FIELD_NUMBER: _ClassVar[int]
        address_mode: Config.NetworkConfig.AddressMode
        enabled_protocols: int
        eth_enabled: bool
        ipv4_config: Config.NetworkConfig.IpV4Config
        ipv6_enabled: bool
        ntp_server: str
        rsyslog_server: str
        wifi_enabled: bool
        wifi_psk: str
        wifi_ssid: str
        def __init__(self, wifi_enabled: bool = ..., wifi_ssid: _Optional[str] = ..., wifi_psk: _Optional[str] = ..., ntp_server: _Optional[str] = ..., eth_enabled: bool = ..., address_mode: _Optional[_Union[Config.NetworkConfig.AddressMode, str]] = ..., ipv4_config: _Optional[_Union[Config.NetworkConfig.IpV4Config, _Mapping]] = ..., rsyslog_server: _Optional[str] = ..., enabled_protocols: _Optional[int] = ..., ipv6_enabled: bool = ...) -> None: ...
    class PositionConfig(_message.Message):
        __slots__ = ["broadcast_smart_minimum_distance", "broadcast_smart_minimum_interval_secs", "fixed_position", "gps_attempt_time", "gps_en_gpio", "gps_enabled", "gps_mode", "gps_update_interval", "position_broadcast_secs", "position_broadcast_smart_enabled", "position_flags", "rx_gpio", "tx_gpio"]
        class GpsMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class PositionFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ALTITUDE: Config.PositionConfig.PositionFlags
        ALTITUDE_MSL: Config.PositionConfig.PositionFlags
        BROADCAST_SMART_MINIMUM_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_SMART_MINIMUM_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
        DISABLED: Config.PositionConfig.GpsMode
        DOP: Config.PositionConfig.PositionFlags
        ENABLED: Config.PositionConfig.GpsMode
        FIXED_POSITION_FIELD_NUMBER: _ClassVar[int]
        GEOIDAL_SEPARATION: Config.PositionConfig.PositionFlags
        GPS_ATTEMPT_TIME_FIELD_NUMBER: _ClassVar[int]
        GPS_ENABLED_FIELD_NUMBER: _ClassVar[int]
        GPS_EN_GPIO_FIELD_NUMBER: _ClassVar[int]
        GPS_MODE_FIELD_NUMBER: _ClassVar[int]
        GPS_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        HEADING: Config.PositionConfig.PositionFlags
        HVDOP: Config.PositionConfig.PositionFlags
        NOT_PRESENT: Config.PositionConfig.GpsMode
        POSITION_BROADCAST_SECS_FIELD_NUMBER: _ClassVar[int]
        POSITION_BROADCAST_SMART_ENABLED_FIELD_NUMBER: _ClassVar[int]
        POSITION_FLAGS_FIELD_NUMBER: _ClassVar[int]
        RX_GPIO_FIELD_NUMBER: _ClassVar[int]
        SATINVIEW: Config.PositionConfig.PositionFlags
        SEQ_NO: Config.PositionConfig.PositionFlags
        SPEED: Config.PositionConfig.PositionFlags
        TIMESTAMP: Config.PositionConfig.PositionFlags
        TX_GPIO_FIELD_NUMBER: _ClassVar[int]
        UNSET: Config.PositionConfig.PositionFlags
        broadcast_smart_minimum_distance: int
        broadcast_smart_minimum_interval_secs: int
        fixed_position: bool
        gps_attempt_time: int
        gps_en_gpio: int
        gps_enabled: bool
        gps_mode: Config.PositionConfig.GpsMode
        gps_update_interval: int
        position_broadcast_secs: int
        position_broadcast_smart_enabled: bool
        position_flags: int
        rx_gpio: int
        tx_gpio: int
        def __init__(self, position_broadcast_secs: _Optional[int] = ..., position_broadcast_smart_enabled: bool = ..., fixed_position: bool = ..., gps_enabled: bool = ..., gps_update_interval: _Optional[int] = ..., gps_attempt_time: _Optional[int] = ..., position_flags: _Optional[int] = ..., rx_gpio: _Optional[int] = ..., tx_gpio: _Optional[int] = ..., broadcast_smart_minimum_distance: _Optional[int] = ..., broadcast_smart_minimum_interval_secs: _Optional[int] = ..., gps_en_gpio: _Optional[int] = ..., gps_mode: _Optional[_Union[Config.PositionConfig.GpsMode, str]] = ...) -> None: ...
    class PowerConfig(_message.Message):
        __slots__ = ["adc_multiplier_override", "device_battery_ina_address", "is_power_saving", "ls_secs", "min_wake_secs", "on_battery_shutdown_after_secs", "powermon_enables", "sds_secs", "wait_bluetooth_secs"]
        ADC_MULTIPLIER_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
        DEVICE_BATTERY_INA_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        IS_POWER_SAVING_FIELD_NUMBER: _ClassVar[int]
        LS_SECS_FIELD_NUMBER: _ClassVar[int]
        MIN_WAKE_SECS_FIELD_NUMBER: _ClassVar[int]
        ON_BATTERY_SHUTDOWN_AFTER_SECS_FIELD_NUMBER: _ClassVar[int]
        POWERMON_ENABLES_FIELD_NUMBER: _ClassVar[int]
        SDS_SECS_FIELD_NUMBER: _ClassVar[int]
        WAIT_BLUETOOTH_SECS_FIELD_NUMBER: _ClassVar[int]
        adc_multiplier_override: float
        device_battery_ina_address: int
        is_power_saving: bool
        ls_secs: int
        min_wake_secs: int
        on_battery_shutdown_after_secs: int
        powermon_enables: int
        sds_secs: int
        wait_bluetooth_secs: int
        def __init__(self, is_power_saving: bool = ..., on_battery_shutdown_after_secs: _Optional[int] = ..., adc_multiplier_override: _Optional[float] = ..., wait_bluetooth_secs: _Optional[int] = ..., sds_secs: _Optional[int] = ..., ls_secs: _Optional[int] = ..., min_wake_secs: _Optional[int] = ..., device_battery_ina_address: _Optional[int] = ..., powermon_enables: _Optional[int] = ...) -> None: ...
    class SecurityConfig(_message.Message):
        __slots__ = ["admin_channel_enabled", "admin_key", "debug_log_api_enabled", "is_managed", "packet_signature_policy", "private_key", "public_key", "serial_enabled"]
        class PacketSignaturePolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ADMIN_CHANNEL_ENABLED_FIELD_NUMBER: _ClassVar[int]
        ADMIN_KEY_FIELD_NUMBER: _ClassVar[int]
        DEBUG_LOG_API_ENABLED_FIELD_NUMBER: _ClassVar[int]
        IS_MANAGED_FIELD_NUMBER: _ClassVar[int]
        PACKET_SIGNATURE_POLICY_BALANCED: Config.SecurityConfig.PacketSignaturePolicy
        PACKET_SIGNATURE_POLICY_COMPATIBLE: Config.SecurityConfig.PacketSignaturePolicy
        PACKET_SIGNATURE_POLICY_FIELD_NUMBER: _ClassVar[int]
        PACKET_SIGNATURE_POLICY_STRICT: Config.SecurityConfig.PacketSignaturePolicy
        PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
        SERIAL_ENABLED_FIELD_NUMBER: _ClassVar[int]
        admin_channel_enabled: bool
        admin_key: _containers.RepeatedScalarFieldContainer[bytes]
        debug_log_api_enabled: bool
        is_managed: bool
        packet_signature_policy: Config.SecurityConfig.PacketSignaturePolicy
        private_key: bytes
        public_key: bytes
        serial_enabled: bool
        def __init__(self, public_key: _Optional[bytes] = ..., private_key: _Optional[bytes] = ..., admin_key: _Optional[_Iterable[bytes]] = ..., is_managed: bool = ..., serial_enabled: bool = ..., debug_log_api_enabled: bool = ..., admin_channel_enabled: bool = ..., packet_signature_policy: _Optional[_Union[Config.SecurityConfig.PacketSignaturePolicy, str]] = ...) -> None: ...
    class SessionkeyConfig(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    BLUETOOTH_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_UI_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    LORA_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    SESSIONKEY_FIELD_NUMBER: _ClassVar[int]
    bluetooth: Config.BluetoothConfig
    device: Config.DeviceConfig
    device_ui: _device_ui_pb2.DeviceUIConfig
    display: Config.DisplayConfig
    lora: Config.LoRaConfig
    network: Config.NetworkConfig
    position: Config.PositionConfig
    power: Config.PowerConfig
    security: Config.SecurityConfig
    sessionkey: Config.SessionkeyConfig
    def __init__(self, device: _Optional[_Union[Config.DeviceConfig, _Mapping]] = ..., position: _Optional[_Union[Config.PositionConfig, _Mapping]] = ..., power: _Optional[_Union[Config.PowerConfig, _Mapping]] = ..., network: _Optional[_Union[Config.NetworkConfig, _Mapping]] = ..., display: _Optional[_Union[Config.DisplayConfig, _Mapping]] = ..., lora: _Optional[_Union[Config.LoRaConfig, _Mapping]] = ..., bluetooth: _Optional[_Union[Config.BluetoothConfig, _Mapping]] = ..., security: _Optional[_Union[Config.SecurityConfig, _Mapping]] = ..., sessionkey: _Optional[_Union[Config.SessionkeyConfig, _Mapping]] = ..., device_ui: _Optional[_Union[_device_ui_pb2.DeviceUIConfig, _Mapping]] = ...) -> None: ...
