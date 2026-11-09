from meshtastic.protobuf import atak_pb2 as _atak_pb2
from meshtastic.protobuf import channel_pb2 as _channel_pb2
from meshtastic.protobuf import config_pb2 as _config_pb2
from meshtastic.protobuf import field_metadata_pb2 as _field_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
DIGITAL_READ: RemoteHardwarePinType
DIGITAL_WRITE: RemoteHardwarePinType
UNKNOWN: RemoteHardwarePinType

class ModuleConfig(_message.Message):
    __slots__ = ["ambient_lighting", "audio", "canned_message", "detection_sensor", "external_notification", "mesh_beacon", "mqtt", "neighbor_info", "paxcounter", "range_test", "remote_hardware", "serial", "statusmessage", "store_forward", "tak", "telemetry", "traffic_management"]
    class AmbientLightingConfig(_message.Message):
        __slots__ = ["blue", "current", "green", "led_state", "red"]
        BLUE_FIELD_NUMBER: _ClassVar[int]
        CURRENT_FIELD_NUMBER: _ClassVar[int]
        GREEN_FIELD_NUMBER: _ClassVar[int]
        LED_STATE_FIELD_NUMBER: _ClassVar[int]
        RED_FIELD_NUMBER: _ClassVar[int]
        blue: int
        current: int
        green: int
        led_state: bool
        red: int
        def __init__(self, led_state: bool = ..., current: _Optional[int] = ..., red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ...) -> None: ...
    class AudioConfig(_message.Message):
        __slots__ = ["bitrate", "codec2_enabled", "i2s_din", "i2s_sck", "i2s_sd", "i2s_ws", "ptt_pin"]
        class Audio_Baud(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        BITRATE_FIELD_NUMBER: _ClassVar[int]
        CODEC2_1200: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_1300: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_1400: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_1600: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_2400: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_3200: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_450: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_700: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_700B: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_700C: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_DEFAULT: ModuleConfig.AudioConfig.Audio_Baud
        CODEC2_ENABLED_FIELD_NUMBER: _ClassVar[int]
        I2S_DIN_FIELD_NUMBER: _ClassVar[int]
        I2S_SCK_FIELD_NUMBER: _ClassVar[int]
        I2S_SD_FIELD_NUMBER: _ClassVar[int]
        I2S_WS_FIELD_NUMBER: _ClassVar[int]
        PTT_PIN_FIELD_NUMBER: _ClassVar[int]
        bitrate: ModuleConfig.AudioConfig.Audio_Baud
        codec2_enabled: bool
        i2s_din: int
        i2s_sck: int
        i2s_sd: int
        i2s_ws: int
        ptt_pin: int
        def __init__(self, codec2_enabled: bool = ..., ptt_pin: _Optional[int] = ..., bitrate: _Optional[_Union[ModuleConfig.AudioConfig.Audio_Baud, str]] = ..., i2s_ws: _Optional[int] = ..., i2s_sd: _Optional[int] = ..., i2s_din: _Optional[int] = ..., i2s_sck: _Optional[int] = ...) -> None: ...
    class CannedMessageConfig(_message.Message):
        __slots__ = ["allow_input_source", "enabled", "inputbroker_event_ccw", "inputbroker_event_cw", "inputbroker_event_press", "inputbroker_pin_a", "inputbroker_pin_b", "inputbroker_pin_press", "rotary1_enabled", "send_bell", "updown1_enabled"]
        class InputEventChar(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ALLOW_INPUT_SOURCE_FIELD_NUMBER: _ClassVar[int]
        BACK: ModuleConfig.CannedMessageConfig.InputEventChar
        CANCEL: ModuleConfig.CannedMessageConfig.InputEventChar
        DOWN: ModuleConfig.CannedMessageConfig.InputEventChar
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_EVENT_CCW_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_EVENT_CW_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_EVENT_PRESS_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_PIN_A_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_PIN_B_FIELD_NUMBER: _ClassVar[int]
        INPUTBROKER_PIN_PRESS_FIELD_NUMBER: _ClassVar[int]
        LEFT: ModuleConfig.CannedMessageConfig.InputEventChar
        NONE: ModuleConfig.CannedMessageConfig.InputEventChar
        RIGHT: ModuleConfig.CannedMessageConfig.InputEventChar
        ROTARY1_ENABLED_FIELD_NUMBER: _ClassVar[int]
        SELECT: ModuleConfig.CannedMessageConfig.InputEventChar
        SEND_BELL_FIELD_NUMBER: _ClassVar[int]
        UP: ModuleConfig.CannedMessageConfig.InputEventChar
        UPDOWN1_ENABLED_FIELD_NUMBER: _ClassVar[int]
        allow_input_source: str
        enabled: bool
        inputbroker_event_ccw: ModuleConfig.CannedMessageConfig.InputEventChar
        inputbroker_event_cw: ModuleConfig.CannedMessageConfig.InputEventChar
        inputbroker_event_press: ModuleConfig.CannedMessageConfig.InputEventChar
        inputbroker_pin_a: int
        inputbroker_pin_b: int
        inputbroker_pin_press: int
        rotary1_enabled: bool
        send_bell: bool
        updown1_enabled: bool
        def __init__(self, rotary1_enabled: bool = ..., inputbroker_pin_a: _Optional[int] = ..., inputbroker_pin_b: _Optional[int] = ..., inputbroker_pin_press: _Optional[int] = ..., inputbroker_event_cw: _Optional[_Union[ModuleConfig.CannedMessageConfig.InputEventChar, str]] = ..., inputbroker_event_ccw: _Optional[_Union[ModuleConfig.CannedMessageConfig.InputEventChar, str]] = ..., inputbroker_event_press: _Optional[_Union[ModuleConfig.CannedMessageConfig.InputEventChar, str]] = ..., updown1_enabled: bool = ..., enabled: bool = ..., allow_input_source: _Optional[str] = ..., send_bell: bool = ...) -> None: ...
    class DetectionSensorConfig(_message.Message):
        __slots__ = ["detection_trigger_type", "enabled", "minimum_broadcast_secs", "monitor_pin", "name", "send_bell", "state_broadcast_secs", "use_pullup"]
        class TriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        DETECTION_TRIGGER_TYPE_FIELD_NUMBER: _ClassVar[int]
        EITHER_EDGE_ACTIVE_HIGH: ModuleConfig.DetectionSensorConfig.TriggerType
        EITHER_EDGE_ACTIVE_LOW: ModuleConfig.DetectionSensorConfig.TriggerType
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        FALLING_EDGE: ModuleConfig.DetectionSensorConfig.TriggerType
        LOGIC_HIGH: ModuleConfig.DetectionSensorConfig.TriggerType
        LOGIC_LOW: ModuleConfig.DetectionSensorConfig.TriggerType
        MINIMUM_BROADCAST_SECS_FIELD_NUMBER: _ClassVar[int]
        MONITOR_PIN_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        RISING_EDGE: ModuleConfig.DetectionSensorConfig.TriggerType
        SEND_BELL_FIELD_NUMBER: _ClassVar[int]
        STATE_BROADCAST_SECS_FIELD_NUMBER: _ClassVar[int]
        USE_PULLUP_FIELD_NUMBER: _ClassVar[int]
        detection_trigger_type: ModuleConfig.DetectionSensorConfig.TriggerType
        enabled: bool
        minimum_broadcast_secs: int
        monitor_pin: int
        name: str
        send_bell: bool
        state_broadcast_secs: int
        use_pullup: bool
        def __init__(self, enabled: bool = ..., minimum_broadcast_secs: _Optional[int] = ..., state_broadcast_secs: _Optional[int] = ..., send_bell: bool = ..., name: _Optional[str] = ..., monitor_pin: _Optional[int] = ..., detection_trigger_type: _Optional[_Union[ModuleConfig.DetectionSensorConfig.TriggerType, str]] = ..., use_pullup: bool = ...) -> None: ...
    class ExternalNotificationConfig(_message.Message):
        __slots__ = ["active", "alert_bell", "alert_bell_buzzer", "alert_bell_vibra", "alert_message", "alert_message_buzzer", "alert_message_vibra", "enabled", "nag_timeout", "output", "output_buzzer", "output_ms", "output_vibra", "use_i2s_as_buzzer", "use_pwm"]
        ACTIVE_FIELD_NUMBER: _ClassVar[int]
        ALERT_BELL_BUZZER_FIELD_NUMBER: _ClassVar[int]
        ALERT_BELL_FIELD_NUMBER: _ClassVar[int]
        ALERT_BELL_VIBRA_FIELD_NUMBER: _ClassVar[int]
        ALERT_MESSAGE_BUZZER_FIELD_NUMBER: _ClassVar[int]
        ALERT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        ALERT_MESSAGE_VIBRA_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        NAG_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_BUZZER_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_MS_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_VIBRA_FIELD_NUMBER: _ClassVar[int]
        USE_I2S_AS_BUZZER_FIELD_NUMBER: _ClassVar[int]
        USE_PWM_FIELD_NUMBER: _ClassVar[int]
        active: bool
        alert_bell: bool
        alert_bell_buzzer: bool
        alert_bell_vibra: bool
        alert_message: bool
        alert_message_buzzer: bool
        alert_message_vibra: bool
        enabled: bool
        nag_timeout: int
        output: int
        output_buzzer: int
        output_ms: int
        output_vibra: int
        use_i2s_as_buzzer: bool
        use_pwm: bool
        def __init__(self, enabled: bool = ..., output_ms: _Optional[int] = ..., output: _Optional[int] = ..., output_vibra: _Optional[int] = ..., output_buzzer: _Optional[int] = ..., active: bool = ..., alert_message: bool = ..., alert_message_vibra: bool = ..., alert_message_buzzer: bool = ..., alert_bell: bool = ..., alert_bell_vibra: bool = ..., alert_bell_buzzer: bool = ..., use_pwm: bool = ..., nag_timeout: _Optional[int] = ..., use_i2s_as_buzzer: bool = ...) -> None: ...
    class MQTTConfig(_message.Message):
        __slots__ = ["address", "enabled", "encryption_enabled", "json_enabled", "map_report_settings", "map_reporting_enabled", "password", "proxy_to_client_enabled", "root", "tls_enabled", "username"]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        ENCRYPTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
        JSON_ENABLED_FIELD_NUMBER: _ClassVar[int]
        MAP_REPORTING_ENABLED_FIELD_NUMBER: _ClassVar[int]
        MAP_REPORT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        PASSWORD_FIELD_NUMBER: _ClassVar[int]
        PROXY_TO_CLIENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
        ROOT_FIELD_NUMBER: _ClassVar[int]
        TLS_ENABLED_FIELD_NUMBER: _ClassVar[int]
        USERNAME_FIELD_NUMBER: _ClassVar[int]
        address: str
        enabled: bool
        encryption_enabled: bool
        json_enabled: bool
        map_report_settings: ModuleConfig.MapReportSettings
        map_reporting_enabled: bool
        password: str
        proxy_to_client_enabled: bool
        root: str
        tls_enabled: bool
        username: str
        def __init__(self, enabled: bool = ..., address: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., encryption_enabled: bool = ..., json_enabled: bool = ..., tls_enabled: bool = ..., root: _Optional[str] = ..., proxy_to_client_enabled: bool = ..., map_reporting_enabled: bool = ..., map_report_settings: _Optional[_Union[ModuleConfig.MapReportSettings, _Mapping]] = ...) -> None: ...
    class MapReportSettings(_message.Message):
        __slots__ = ["position_precision", "publish_interval_secs", "should_report_location"]
        POSITION_PRECISION_FIELD_NUMBER: _ClassVar[int]
        PUBLISH_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
        SHOULD_REPORT_LOCATION_FIELD_NUMBER: _ClassVar[int]
        position_precision: int
        publish_interval_secs: int
        should_report_location: bool
        def __init__(self, publish_interval_secs: _Optional[int] = ..., position_precision: _Optional[int] = ..., should_report_location: bool = ...) -> None: ...
    class MeshBeaconConfig(_message.Message):
        __slots__ = ["broadcast_interval_secs", "broadcast_message", "broadcast_offer_channel", "broadcast_offer_frequency_slot", "broadcast_offer_preset", "broadcast_offer_region", "broadcast_targets", "flags"]
        class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class BroadcastTarget(_message.Message):
            __slots__ = ["channel_index", "frequency_slot", "preset", "region"]
            CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
            FREQUENCY_SLOT_FIELD_NUMBER: _ClassVar[int]
            PRESET_FIELD_NUMBER: _ClassVar[int]
            REGION_FIELD_NUMBER: _ClassVar[int]
            channel_index: int
            frequency_slot: int
            preset: _config_pb2.Config.LoRaConfig.ModemPreset
            region: _config_pb2.Config.LoRaConfig.RegionCode
            def __init__(self, preset: _Optional[_Union[_config_pb2.Config.LoRaConfig.ModemPreset, str]] = ..., region: _Optional[_Union[_config_pb2.Config.LoRaConfig.RegionCode, str]] = ..., channel_index: _Optional[int] = ..., frequency_slot: _Optional[int] = ...) -> None: ...
        BROADCAST_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_OFFER_CHANNEL_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_OFFER_FREQUENCY_SLOT_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_OFFER_PRESET_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_OFFER_REGION_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_TARGETS_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        FLAG_BROADCAST_ENABLED: ModuleConfig.MeshBeaconConfig.Flags
        FLAG_LEGACY_SPLIT: ModuleConfig.MeshBeaconConfig.Flags
        FLAG_LISTEN_ENABLED: ModuleConfig.MeshBeaconConfig.Flags
        FLAG_NONE: ModuleConfig.MeshBeaconConfig.Flags
        broadcast_interval_secs: int
        broadcast_message: str
        broadcast_offer_channel: _channel_pb2.ChannelSettings
        broadcast_offer_frequency_slot: int
        broadcast_offer_preset: _config_pb2.Config.LoRaConfig.ModemPreset
        broadcast_offer_region: _config_pb2.Config.LoRaConfig.RegionCode
        broadcast_targets: _containers.RepeatedCompositeFieldContainer[ModuleConfig.MeshBeaconConfig.BroadcastTarget]
        flags: int
        def __init__(self, flags: _Optional[int] = ..., broadcast_offer_frequency_slot: _Optional[int] = ..., broadcast_message: _Optional[str] = ..., broadcast_offer_channel: _Optional[_Union[_channel_pb2.ChannelSettings, _Mapping]] = ..., broadcast_offer_region: _Optional[_Union[_config_pb2.Config.LoRaConfig.RegionCode, str]] = ..., broadcast_offer_preset: _Optional[_Union[_config_pb2.Config.LoRaConfig.ModemPreset, str]] = ..., broadcast_interval_secs: _Optional[int] = ..., broadcast_targets: _Optional[_Iterable[_Union[ModuleConfig.MeshBeaconConfig.BroadcastTarget, _Mapping]]] = ...) -> None: ...
    class NeighborInfoConfig(_message.Message):
        __slots__ = ["enabled", "transmit_over_lora", "update_interval"]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        TRANSMIT_OVER_LORA_FIELD_NUMBER: _ClassVar[int]
        UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        transmit_over_lora: bool
        update_interval: int
        def __init__(self, enabled: bool = ..., update_interval: _Optional[int] = ..., transmit_over_lora: bool = ...) -> None: ...
    class PaxcounterConfig(_message.Message):
        __slots__ = ["ble_threshold", "enabled", "paxcounter_update_interval", "wifi_threshold"]
        BLE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        PAXCOUNTER_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        WIFI_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        ble_threshold: int
        enabled: bool
        paxcounter_update_interval: int
        wifi_threshold: int
        def __init__(self, enabled: bool = ..., paxcounter_update_interval: _Optional[int] = ..., wifi_threshold: _Optional[int] = ..., ble_threshold: _Optional[int] = ...) -> None: ...
    class RangeTestConfig(_message.Message):
        __slots__ = ["clear_on_reboot", "enabled", "save", "sender"]
        CLEAR_ON_REBOOT_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        SAVE_FIELD_NUMBER: _ClassVar[int]
        SENDER_FIELD_NUMBER: _ClassVar[int]
        clear_on_reboot: bool
        enabled: bool
        save: bool
        sender: int
        def __init__(self, enabled: bool = ..., sender: _Optional[int] = ..., save: bool = ..., clear_on_reboot: bool = ...) -> None: ...
    class RemoteHardwareConfig(_message.Message):
        __slots__ = ["allow_undefined_pin_access", "available_pins", "enabled"]
        ALLOW_UNDEFINED_PIN_ACCESS_FIELD_NUMBER: _ClassVar[int]
        AVAILABLE_PINS_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        allow_undefined_pin_access: bool
        available_pins: _containers.RepeatedCompositeFieldContainer[RemoteHardwarePin]
        enabled: bool
        def __init__(self, enabled: bool = ..., allow_undefined_pin_access: bool = ..., available_pins: _Optional[_Iterable[_Union[RemoteHardwarePin, _Mapping]]] = ...) -> None: ...
    class SerialConfig(_message.Message):
        __slots__ = ["baud", "echo", "enabled", "mode", "override_console_serial_port", "rxd", "timeout", "txd"]
        class Serial_Baud(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        class Serial_Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        BAUD_110: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_115200: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_1200: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_19200: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_230400: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_2400: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_300: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_38400: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_460800: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_4800: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_57600: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_576000: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_600: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_921600: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_9600: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_DEFAULT: ModuleConfig.SerialConfig.Serial_Baud
        BAUD_FIELD_NUMBER: _ClassVar[int]
        CALTOPO: ModuleConfig.SerialConfig.Serial_Mode
        DEFAULT: ModuleConfig.SerialConfig.Serial_Mode
        ECHO_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        LOG: ModuleConfig.SerialConfig.Serial_Mode
        LOGTEXT: ModuleConfig.SerialConfig.Serial_Mode
        MODBUS: ModuleConfig.SerialConfig.Serial_Mode
        MODE_FIELD_NUMBER: _ClassVar[int]
        MS_CONFIG: ModuleConfig.SerialConfig.Serial_Mode
        NMEA: ModuleConfig.SerialConfig.Serial_Mode
        OVERRIDE_CONSOLE_SERIAL_PORT_FIELD_NUMBER: _ClassVar[int]
        PROTO: ModuleConfig.SerialConfig.Serial_Mode
        RXD_FIELD_NUMBER: _ClassVar[int]
        SIMPLE: ModuleConfig.SerialConfig.Serial_Mode
        TEXTMSG: ModuleConfig.SerialConfig.Serial_Mode
        TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        TXD_FIELD_NUMBER: _ClassVar[int]
        VE_DIRECT: ModuleConfig.SerialConfig.Serial_Mode
        WS85: ModuleConfig.SerialConfig.Serial_Mode
        baud: ModuleConfig.SerialConfig.Serial_Baud
        echo: bool
        enabled: bool
        mode: ModuleConfig.SerialConfig.Serial_Mode
        override_console_serial_port: bool
        rxd: int
        timeout: int
        txd: int
        def __init__(self, enabled: bool = ..., echo: bool = ..., rxd: _Optional[int] = ..., txd: _Optional[int] = ..., baud: _Optional[_Union[ModuleConfig.SerialConfig.Serial_Baud, str]] = ..., timeout: _Optional[int] = ..., mode: _Optional[_Union[ModuleConfig.SerialConfig.Serial_Mode, str]] = ..., override_console_serial_port: bool = ...) -> None: ...
    class StatusMessageConfig(_message.Message):
        __slots__ = ["node_status"]
        NODE_STATUS_FIELD_NUMBER: _ClassVar[int]
        node_status: str
        def __init__(self, node_status: _Optional[str] = ...) -> None: ...
    class StoreForwardConfig(_message.Message):
        __slots__ = ["enabled", "heartbeat", "history_return_max", "history_return_window", "is_server", "records"]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
        HISTORY_RETURN_MAX_FIELD_NUMBER: _ClassVar[int]
        HISTORY_RETURN_WINDOW_FIELD_NUMBER: _ClassVar[int]
        IS_SERVER_FIELD_NUMBER: _ClassVar[int]
        RECORDS_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        heartbeat: bool
        history_return_max: int
        history_return_window: int
        is_server: bool
        records: int
        def __init__(self, enabled: bool = ..., heartbeat: bool = ..., records: _Optional[int] = ..., history_return_max: _Optional[int] = ..., history_return_window: _Optional[int] = ..., is_server: bool = ...) -> None: ...
    class TAKConfig(_message.Message):
        __slots__ = ["role", "team"]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        role: _atak_pb2.MemberRole
        team: _atak_pb2.Team
        def __init__(self, team: _Optional[_Union[_atak_pb2.Team, str]] = ..., role: _Optional[_Union[_atak_pb2.MemberRole, str]] = ...) -> None: ...
    class TelemetryConfig(_message.Message):
        __slots__ = ["air_quality_enabled", "air_quality_interval", "air_quality_screen_enabled", "device_telemetry_enabled", "device_update_interval", "environment_display_fahrenheit", "environment_measurement_enabled", "environment_screen_enabled", "environment_update_interval", "health_measurement_enabled", "health_screen_enabled", "health_update_interval", "power_measurement_enabled", "power_screen_enabled", "power_update_interval"]
        AIR_QUALITY_ENABLED_FIELD_NUMBER: _ClassVar[int]
        AIR_QUALITY_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        AIR_QUALITY_SCREEN_ENABLED_FIELD_NUMBER: _ClassVar[int]
        DEVICE_TELEMETRY_ENABLED_FIELD_NUMBER: _ClassVar[int]
        DEVICE_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_DISPLAY_FAHRENHEIT_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_MEASUREMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_SCREEN_ENABLED_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        HEALTH_MEASUREMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
        HEALTH_SCREEN_ENABLED_FIELD_NUMBER: _ClassVar[int]
        HEALTH_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        POWER_MEASUREMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
        POWER_SCREEN_ENABLED_FIELD_NUMBER: _ClassVar[int]
        POWER_UPDATE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        air_quality_enabled: bool
        air_quality_interval: int
        air_quality_screen_enabled: bool
        device_telemetry_enabled: bool
        device_update_interval: int
        environment_display_fahrenheit: bool
        environment_measurement_enabled: bool
        environment_screen_enabled: bool
        environment_update_interval: int
        health_measurement_enabled: bool
        health_screen_enabled: bool
        health_update_interval: int
        power_measurement_enabled: bool
        power_screen_enabled: bool
        power_update_interval: int
        def __init__(self, device_update_interval: _Optional[int] = ..., environment_update_interval: _Optional[int] = ..., environment_measurement_enabled: bool = ..., environment_screen_enabled: bool = ..., environment_display_fahrenheit: bool = ..., air_quality_enabled: bool = ..., air_quality_interval: _Optional[int] = ..., power_measurement_enabled: bool = ..., power_update_interval: _Optional[int] = ..., power_screen_enabled: bool = ..., health_measurement_enabled: bool = ..., health_update_interval: _Optional[int] = ..., health_screen_enabled: bool = ..., device_telemetry_enabled: bool = ..., air_quality_screen_enabled: bool = ...) -> None: ...
    class TrafficManagementConfig(_message.Message):
        __slots__ = ["nodeinfo_direct_response_max_hops", "position_min_interval_secs", "rate_limit_max_packets", "rate_limit_window_secs", "unknown_packet_threshold"]
        NODEINFO_DIRECT_RESPONSE_MAX_HOPS_FIELD_NUMBER: _ClassVar[int]
        POSITION_MIN_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
        RATE_LIMIT_MAX_PACKETS_FIELD_NUMBER: _ClassVar[int]
        RATE_LIMIT_WINDOW_SECS_FIELD_NUMBER: _ClassVar[int]
        UNKNOWN_PACKET_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        nodeinfo_direct_response_max_hops: int
        position_min_interval_secs: int
        rate_limit_max_packets: int
        rate_limit_window_secs: int
        unknown_packet_threshold: int
        def __init__(self, position_min_interval_secs: _Optional[int] = ..., nodeinfo_direct_response_max_hops: _Optional[int] = ..., rate_limit_window_secs: _Optional[int] = ..., rate_limit_max_packets: _Optional[int] = ..., unknown_packet_threshold: _Optional[int] = ...) -> None: ...
    AMBIENT_LIGHTING_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    CANNED_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETECTION_SENSOR_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    MESH_BEACON_FIELD_NUMBER: _ClassVar[int]
    MQTT_FIELD_NUMBER: _ClassVar[int]
    NEIGHBOR_INFO_FIELD_NUMBER: _ClassVar[int]
    PAXCOUNTER_FIELD_NUMBER: _ClassVar[int]
    RANGE_TEST_FIELD_NUMBER: _ClassVar[int]
    REMOTE_HARDWARE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    STATUSMESSAGE_FIELD_NUMBER: _ClassVar[int]
    STORE_FORWARD_FIELD_NUMBER: _ClassVar[int]
    TAK_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    ambient_lighting: ModuleConfig.AmbientLightingConfig
    audio: ModuleConfig.AudioConfig
    canned_message: ModuleConfig.CannedMessageConfig
    detection_sensor: ModuleConfig.DetectionSensorConfig
    external_notification: ModuleConfig.ExternalNotificationConfig
    mesh_beacon: ModuleConfig.MeshBeaconConfig
    mqtt: ModuleConfig.MQTTConfig
    neighbor_info: ModuleConfig.NeighborInfoConfig
    paxcounter: ModuleConfig.PaxcounterConfig
    range_test: ModuleConfig.RangeTestConfig
    remote_hardware: ModuleConfig.RemoteHardwareConfig
    serial: ModuleConfig.SerialConfig
    statusmessage: ModuleConfig.StatusMessageConfig
    store_forward: ModuleConfig.StoreForwardConfig
    tak: ModuleConfig.TAKConfig
    telemetry: ModuleConfig.TelemetryConfig
    traffic_management: ModuleConfig.TrafficManagementConfig
    def __init__(self, mqtt: _Optional[_Union[ModuleConfig.MQTTConfig, _Mapping]] = ..., serial: _Optional[_Union[ModuleConfig.SerialConfig, _Mapping]] = ..., external_notification: _Optional[_Union[ModuleConfig.ExternalNotificationConfig, _Mapping]] = ..., store_forward: _Optional[_Union[ModuleConfig.StoreForwardConfig, _Mapping]] = ..., range_test: _Optional[_Union[ModuleConfig.RangeTestConfig, _Mapping]] = ..., telemetry: _Optional[_Union[ModuleConfig.TelemetryConfig, _Mapping]] = ..., canned_message: _Optional[_Union[ModuleConfig.CannedMessageConfig, _Mapping]] = ..., audio: _Optional[_Union[ModuleConfig.AudioConfig, _Mapping]] = ..., remote_hardware: _Optional[_Union[ModuleConfig.RemoteHardwareConfig, _Mapping]] = ..., neighbor_info: _Optional[_Union[ModuleConfig.NeighborInfoConfig, _Mapping]] = ..., ambient_lighting: _Optional[_Union[ModuleConfig.AmbientLightingConfig, _Mapping]] = ..., detection_sensor: _Optional[_Union[ModuleConfig.DetectionSensorConfig, _Mapping]] = ..., paxcounter: _Optional[_Union[ModuleConfig.PaxcounterConfig, _Mapping]] = ..., statusmessage: _Optional[_Union[ModuleConfig.StatusMessageConfig, _Mapping]] = ..., traffic_management: _Optional[_Union[ModuleConfig.TrafficManagementConfig, _Mapping]] = ..., tak: _Optional[_Union[ModuleConfig.TAKConfig, _Mapping]] = ..., mesh_beacon: _Optional[_Union[ModuleConfig.MeshBeaconConfig, _Mapping]] = ...) -> None: ...

class RemoteHardwarePin(_message.Message):
    __slots__ = ["gpio_pin", "name", "type"]
    GPIO_PIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    gpio_pin: int
    name: str
    type: RemoteHardwarePinType
    def __init__(self, gpio_pin: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[_Union[RemoteHardwarePinType, str]] = ...) -> None: ...

class RemoteHardwarePinType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
