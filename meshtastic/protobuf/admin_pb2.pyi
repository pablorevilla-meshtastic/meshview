from meshtastic.protobuf import channel_pb2 as _channel_pb2
from meshtastic.protobuf import config_pb2 as _config_pb2
from meshtastic.protobuf import connection_status_pb2 as _connection_status_pb2
from meshtastic.protobuf import device_ui_pb2 as _device_ui_pb2
from meshtastic.protobuf import mesh_pb2 as _mesh_pb2
from meshtastic.protobuf import module_config_pb2 as _module_config_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
NO_REBOOT_OTA: OTAMode
OTA_BLE: OTAMode
OTA_WIFI: OTAMode

class AS3935_config(_message.Message):
    __slots__ = ["set_tuning_cap_pf"]
    SET_TUNING_CAP_PF_FIELD_NUMBER: _ClassVar[int]
    set_tuning_cap_pf: int
    def __init__(self, set_tuning_cap_pf: _Optional[int] = ...) -> None: ...

class AdminMessage(_message.Message):
    __slots__ = ["add_contact", "backup_preferences", "begin_edit_settings", "commit_edit_settings", "delete_file_request", "enter_dfu_mode_request", "exit_simulator", "factory_reset_config", "factory_reset_device", "get_canned_message_module_messages_request", "get_canned_message_module_messages_response", "get_channel_request", "get_channel_response", "get_config_request", "get_config_response", "get_device_connection_status_request", "get_device_connection_status_response", "get_device_metadata_request", "get_device_metadata_response", "get_module_config_request", "get_module_config_response", "get_node_remote_hardware_pins_request", "get_node_remote_hardware_pins_response", "get_owner_request", "get_owner_response", "get_ringtone_request", "get_ringtone_response", "get_ui_config_request", "get_ui_config_response", "key_verification", "lockdown_auth", "nodedb_reset", "ota_request", "reboot_ota_seconds", "reboot_seconds", "remove_backup_preferences", "remove_by_nodenum", "remove_favorite_node", "remove_fixed_position", "remove_ignored_node", "restore_preferences", "send_input_event", "sensor_config", "session_passkey", "set_canned_message_module_messages", "set_channel", "set_config", "set_favorite_node", "set_fixed_position", "set_ham_mode", "set_ignored_node", "set_module_config", "set_owner", "set_ringtone_message", "set_scale", "set_time_only", "shutdown_seconds", "store_ui_config", "toggle_muted_node"]
    class BackupLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ConfigType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ModuleConfigType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class InputEvent(_message.Message):
        __slots__ = ["event_code", "kb_char", "touch_x", "touch_y"]
        EVENT_CODE_FIELD_NUMBER: _ClassVar[int]
        KB_CHAR_FIELD_NUMBER: _ClassVar[int]
        TOUCH_X_FIELD_NUMBER: _ClassVar[int]
        TOUCH_Y_FIELD_NUMBER: _ClassVar[int]
        event_code: int
        kb_char: int
        touch_x: int
        touch_y: int
        def __init__(self, event_code: _Optional[int] = ..., kb_char: _Optional[int] = ..., touch_x: _Optional[int] = ..., touch_y: _Optional[int] = ...) -> None: ...
    class OTAEvent(_message.Message):
        __slots__ = ["ota_hash", "reboot_ota_mode"]
        OTA_HASH_FIELD_NUMBER: _ClassVar[int]
        REBOOT_OTA_MODE_FIELD_NUMBER: _ClassVar[int]
        ota_hash: bytes
        reboot_ota_mode: OTAMode
        def __init__(self, reboot_ota_mode: _Optional[_Union[OTAMode, str]] = ..., ota_hash: _Optional[bytes] = ...) -> None: ...
    ADD_CONTACT_FIELD_NUMBER: _ClassVar[int]
    AMBIENTLIGHTING_CONFIG: AdminMessage.ModuleConfigType
    AUDIO_CONFIG: AdminMessage.ModuleConfigType
    BACKUP_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    BEGIN_EDIT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    BLUETOOTH_CONFIG: AdminMessage.ConfigType
    CANNEDMSG_CONFIG: AdminMessage.ModuleConfigType
    COMMIT_EDIT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DELETE_FILE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DETECTIONSENSOR_CONFIG: AdminMessage.ModuleConfigType
    DEVICEUI_CONFIG: AdminMessage.ConfigType
    DEVICE_CONFIG: AdminMessage.ConfigType
    DISPLAY_CONFIG: AdminMessage.ConfigType
    ENTER_DFU_MODE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    EXIT_SIMULATOR_FIELD_NUMBER: _ClassVar[int]
    EXTNOTIF_CONFIG: AdminMessage.ModuleConfigType
    FACTORY_RESET_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FACTORY_RESET_DEVICE_FIELD_NUMBER: _ClassVar[int]
    FLASH: AdminMessage.BackupLocation
    GET_CANNED_MESSAGE_MODULE_MESSAGES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_CANNED_MESSAGE_MODULE_MESSAGES_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_CHANNEL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_CHANNEL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_CONFIG_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_CONFIG_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_DEVICE_CONNECTION_STATUS_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_DEVICE_CONNECTION_STATUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_DEVICE_METADATA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_DEVICE_METADATA_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_MODULE_CONFIG_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_MODULE_CONFIG_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_NODE_REMOTE_HARDWARE_PINS_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_NODE_REMOTE_HARDWARE_PINS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_OWNER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_OWNER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_RINGTONE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_RINGTONE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_UI_CONFIG_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_UI_CONFIG_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    KEY_VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    LOCKDOWN_AUTH_FIELD_NUMBER: _ClassVar[int]
    LORA_CONFIG: AdminMessage.ConfigType
    MESHBEACON_CONFIG: AdminMessage.ModuleConfigType
    MQTT_CONFIG: AdminMessage.ModuleConfigType
    NEIGHBORINFO_CONFIG: AdminMessage.ModuleConfigType
    NETWORK_CONFIG: AdminMessage.ConfigType
    NODEDB_RESET_FIELD_NUMBER: _ClassVar[int]
    OTA_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PAXCOUNTER_CONFIG: AdminMessage.ModuleConfigType
    POSITION_CONFIG: AdminMessage.ConfigType
    POWER_CONFIG: AdminMessage.ConfigType
    RANGETEST_CONFIG: AdminMessage.ModuleConfigType
    REBOOT_OTA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    REBOOT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    REMOTEHARDWARE_CONFIG: AdminMessage.ModuleConfigType
    REMOVE_BACKUP_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    REMOVE_BY_NODENUM_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FAVORITE_NODE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FIXED_POSITION_FIELD_NUMBER: _ClassVar[int]
    REMOVE_IGNORED_NODE_FIELD_NUMBER: _ClassVar[int]
    RESTORE_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    SD: AdminMessage.BackupLocation
    SECURITY_CONFIG: AdminMessage.ConfigType
    SEND_INPUT_EVENT_FIELD_NUMBER: _ClassVar[int]
    SENSOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SERIAL_CONFIG: AdminMessage.ModuleConfigType
    SESSIONKEY_CONFIG: AdminMessage.ConfigType
    SESSION_PASSKEY_FIELD_NUMBER: _ClassVar[int]
    SET_CANNED_MESSAGE_MODULE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SET_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SET_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SET_FAVORITE_NODE_FIELD_NUMBER: _ClassVar[int]
    SET_FIXED_POSITION_FIELD_NUMBER: _ClassVar[int]
    SET_HAM_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_IGNORED_NODE_FIELD_NUMBER: _ClassVar[int]
    SET_MODULE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SET_OWNER_FIELD_NUMBER: _ClassVar[int]
    SET_RINGTONE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SET_SCALE_FIELD_NUMBER: _ClassVar[int]
    SET_TIME_ONLY_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    STATUSMESSAGE_CONFIG: AdminMessage.ModuleConfigType
    STOREFORWARD_CONFIG: AdminMessage.ModuleConfigType
    STORE_UI_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TAK_CONFIG: AdminMessage.ModuleConfigType
    TELEMETRY_CONFIG: AdminMessage.ModuleConfigType
    TOGGLE_MUTED_NODE_FIELD_NUMBER: _ClassVar[int]
    TRAFFICMANAGEMENT_CONFIG: AdminMessage.ModuleConfigType
    add_contact: SharedContact
    backup_preferences: AdminMessage.BackupLocation
    begin_edit_settings: bool
    commit_edit_settings: bool
    delete_file_request: str
    enter_dfu_mode_request: bool
    exit_simulator: bool
    factory_reset_config: int
    factory_reset_device: int
    get_canned_message_module_messages_request: bool
    get_canned_message_module_messages_response: str
    get_channel_request: int
    get_channel_response: _channel_pb2.Channel
    get_config_request: AdminMessage.ConfigType
    get_config_response: _config_pb2.Config
    get_device_connection_status_request: bool
    get_device_connection_status_response: _connection_status_pb2.DeviceConnectionStatus
    get_device_metadata_request: bool
    get_device_metadata_response: _mesh_pb2.DeviceMetadata
    get_module_config_request: AdminMessage.ModuleConfigType
    get_module_config_response: _module_config_pb2.ModuleConfig
    get_node_remote_hardware_pins_request: bool
    get_node_remote_hardware_pins_response: NodeRemoteHardwarePinsResponse
    get_owner_request: bool
    get_owner_response: _mesh_pb2.User
    get_ringtone_request: bool
    get_ringtone_response: str
    get_ui_config_request: bool
    get_ui_config_response: _device_ui_pb2.DeviceUIConfig
    key_verification: KeyVerificationAdmin
    lockdown_auth: LockdownAuth
    nodedb_reset: bool
    ota_request: AdminMessage.OTAEvent
    reboot_ota_seconds: int
    reboot_seconds: int
    remove_backup_preferences: AdminMessage.BackupLocation
    remove_by_nodenum: int
    remove_favorite_node: int
    remove_fixed_position: bool
    remove_ignored_node: int
    restore_preferences: AdminMessage.BackupLocation
    send_input_event: AdminMessage.InputEvent
    sensor_config: SensorConfig
    session_passkey: bytes
    set_canned_message_module_messages: str
    set_channel: _channel_pb2.Channel
    set_config: _config_pb2.Config
    set_favorite_node: int
    set_fixed_position: _mesh_pb2.Position
    set_ham_mode: HamParameters
    set_ignored_node: int
    set_module_config: _module_config_pb2.ModuleConfig
    set_owner: _mesh_pb2.User
    set_ringtone_message: str
    set_scale: int
    set_time_only: int
    shutdown_seconds: int
    store_ui_config: _device_ui_pb2.DeviceUIConfig
    toggle_muted_node: int
    def __init__(self, session_passkey: _Optional[bytes] = ..., get_channel_request: _Optional[int] = ..., get_channel_response: _Optional[_Union[_channel_pb2.Channel, _Mapping]] = ..., get_owner_request: bool = ..., get_owner_response: _Optional[_Union[_mesh_pb2.User, _Mapping]] = ..., get_config_request: _Optional[_Union[AdminMessage.ConfigType, str]] = ..., get_config_response: _Optional[_Union[_config_pb2.Config, _Mapping]] = ..., get_module_config_request: _Optional[_Union[AdminMessage.ModuleConfigType, str]] = ..., get_module_config_response: _Optional[_Union[_module_config_pb2.ModuleConfig, _Mapping]] = ..., get_canned_message_module_messages_request: bool = ..., get_canned_message_module_messages_response: _Optional[str] = ..., get_device_metadata_request: bool = ..., get_device_metadata_response: _Optional[_Union[_mesh_pb2.DeviceMetadata, _Mapping]] = ..., get_ringtone_request: bool = ..., get_ringtone_response: _Optional[str] = ..., get_device_connection_status_request: bool = ..., get_device_connection_status_response: _Optional[_Union[_connection_status_pb2.DeviceConnectionStatus, _Mapping]] = ..., set_ham_mode: _Optional[_Union[HamParameters, _Mapping]] = ..., get_node_remote_hardware_pins_request: bool = ..., get_node_remote_hardware_pins_response: _Optional[_Union[NodeRemoteHardwarePinsResponse, _Mapping]] = ..., enter_dfu_mode_request: bool = ..., delete_file_request: _Optional[str] = ..., set_scale: _Optional[int] = ..., backup_preferences: _Optional[_Union[AdminMessage.BackupLocation, str]] = ..., restore_preferences: _Optional[_Union[AdminMessage.BackupLocation, str]] = ..., remove_backup_preferences: _Optional[_Union[AdminMessage.BackupLocation, str]] = ..., send_input_event: _Optional[_Union[AdminMessage.InputEvent, _Mapping]] = ..., set_owner: _Optional[_Union[_mesh_pb2.User, _Mapping]] = ..., set_channel: _Optional[_Union[_channel_pb2.Channel, _Mapping]] = ..., set_config: _Optional[_Union[_config_pb2.Config, _Mapping]] = ..., set_module_config: _Optional[_Union[_module_config_pb2.ModuleConfig, _Mapping]] = ..., set_canned_message_module_messages: _Optional[str] = ..., set_ringtone_message: _Optional[str] = ..., remove_by_nodenum: _Optional[int] = ..., set_favorite_node: _Optional[int] = ..., remove_favorite_node: _Optional[int] = ..., set_fixed_position: _Optional[_Union[_mesh_pb2.Position, _Mapping]] = ..., remove_fixed_position: bool = ..., set_time_only: _Optional[int] = ..., get_ui_config_request: bool = ..., get_ui_config_response: _Optional[_Union[_device_ui_pb2.DeviceUIConfig, _Mapping]] = ..., store_ui_config: _Optional[_Union[_device_ui_pb2.DeviceUIConfig, _Mapping]] = ..., set_ignored_node: _Optional[int] = ..., remove_ignored_node: _Optional[int] = ..., toggle_muted_node: _Optional[int] = ..., begin_edit_settings: bool = ..., commit_edit_settings: bool = ..., add_contact: _Optional[_Union[SharedContact, _Mapping]] = ..., key_verification: _Optional[_Union[KeyVerificationAdmin, _Mapping]] = ..., factory_reset_device: _Optional[int] = ..., reboot_ota_seconds: _Optional[int] = ..., exit_simulator: bool = ..., reboot_seconds: _Optional[int] = ..., shutdown_seconds: _Optional[int] = ..., factory_reset_config: _Optional[int] = ..., nodedb_reset: bool = ..., ota_request: _Optional[_Union[AdminMessage.OTAEvent, _Mapping]] = ..., sensor_config: _Optional[_Union[SensorConfig, _Mapping]] = ..., lockdown_auth: _Optional[_Union[LockdownAuth, _Mapping]] = ...) -> None: ...

class DS248X_config(_message.Message):
    __slots__ = ["main_temperature_channel"]
    MAIN_TEMPERATURE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    main_temperature_channel: int
    def __init__(self, main_temperature_channel: _Optional[int] = ...) -> None: ...

class HamParameters(_message.Message):
    __slots__ = ["call_sign", "frequency", "long_name", "short_name", "tx_power"]
    CALL_SIGN_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    TX_POWER_FIELD_NUMBER: _ClassVar[int]
    call_sign: str
    frequency: float
    long_name: str
    short_name: str
    tx_power: int
    def __init__(self, call_sign: _Optional[str] = ..., tx_power: _Optional[int] = ..., frequency: _Optional[float] = ..., short_name: _Optional[str] = ..., long_name: _Optional[str] = ...) -> None: ...

class KeyVerificationAdmin(_message.Message):
    __slots__ = ["message_type", "nonce", "remote_nodenum", "security_number"]
    class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DO_NOT_VERIFY: KeyVerificationAdmin.MessageType
    DO_VERIFY: KeyVerificationAdmin.MessageType
    INITIATE_VERIFICATION: KeyVerificationAdmin.MessageType
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    PROVIDE_SECURITY_NUMBER: KeyVerificationAdmin.MessageType
    REMOTE_NODENUM_FIELD_NUMBER: _ClassVar[int]
    SECURITY_NUMBER_FIELD_NUMBER: _ClassVar[int]
    message_type: KeyVerificationAdmin.MessageType
    nonce: int
    remote_nodenum: int
    security_number: int
    def __init__(self, message_type: _Optional[_Union[KeyVerificationAdmin.MessageType, str]] = ..., remote_nodenum: _Optional[int] = ..., nonce: _Optional[int] = ..., security_number: _Optional[int] = ...) -> None: ...

class LockdownAuth(_message.Message):
    __slots__ = ["boots_remaining", "disable", "lock_now", "max_session_seconds", "passphrase", "valid_until_epoch"]
    BOOTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DISABLE_FIELD_NUMBER: _ClassVar[int]
    LOCK_NOW_FIELD_NUMBER: _ClassVar[int]
    MAX_SESSION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    VALID_UNTIL_EPOCH_FIELD_NUMBER: _ClassVar[int]
    boots_remaining: int
    disable: bool
    lock_now: bool
    max_session_seconds: int
    passphrase: bytes
    valid_until_epoch: int
    def __init__(self, passphrase: _Optional[bytes] = ..., boots_remaining: _Optional[int] = ..., valid_until_epoch: _Optional[int] = ..., lock_now: bool = ..., max_session_seconds: _Optional[int] = ..., disable: bool = ...) -> None: ...

class NodeRemoteHardwarePinsResponse(_message.Message):
    __slots__ = ["node_remote_hardware_pins"]
    NODE_REMOTE_HARDWARE_PINS_FIELD_NUMBER: _ClassVar[int]
    node_remote_hardware_pins: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.NodeRemoteHardwarePin]
    def __init__(self, node_remote_hardware_pins: _Optional[_Iterable[_Union[_mesh_pb2.NodeRemoteHardwarePin, _Mapping]]] = ...) -> None: ...

class SCD30_config(_message.Message):
    __slots__ = ["set_altitude", "set_asc", "set_measurement_interval", "set_target_co2_conc", "set_temperature", "soft_reset"]
    SET_ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SET_ASC_FIELD_NUMBER: _ClassVar[int]
    SET_MEASUREMENT_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    SET_TARGET_CO2_CONC_FIELD_NUMBER: _ClassVar[int]
    SET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    SOFT_RESET_FIELD_NUMBER: _ClassVar[int]
    set_altitude: int
    set_asc: bool
    set_measurement_interval: int
    set_target_co2_conc: int
    set_temperature: float
    soft_reset: bool
    def __init__(self, set_asc: bool = ..., set_target_co2_conc: _Optional[int] = ..., set_temperature: _Optional[float] = ..., set_altitude: _Optional[int] = ..., set_measurement_interval: _Optional[int] = ..., soft_reset: bool = ...) -> None: ...

class SCD4X_config(_message.Message):
    __slots__ = ["factory_reset", "set_altitude", "set_ambient_pressure", "set_asc", "set_power_mode", "set_target_co2_conc", "set_temperature"]
    FACTORY_RESET_FIELD_NUMBER: _ClassVar[int]
    SET_ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SET_AMBIENT_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    SET_ASC_FIELD_NUMBER: _ClassVar[int]
    SET_POWER_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_TARGET_CO2_CONC_FIELD_NUMBER: _ClassVar[int]
    SET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    factory_reset: bool
    set_altitude: int
    set_ambient_pressure: int
    set_asc: bool
    set_power_mode: bool
    set_target_co2_conc: int
    set_temperature: float
    def __init__(self, set_asc: bool = ..., set_target_co2_conc: _Optional[int] = ..., set_temperature: _Optional[float] = ..., set_altitude: _Optional[int] = ..., set_ambient_pressure: _Optional[int] = ..., factory_reset: bool = ..., set_power_mode: bool = ...) -> None: ...

class SEN5X_config(_message.Message):
    __slots__ = ["set_one_shot_mode", "set_temperature", "start_fan_cleaning"]
    SET_ONE_SHOT_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    START_FAN_CLEANING_FIELD_NUMBER: _ClassVar[int]
    set_one_shot_mode: bool
    set_temperature: float
    start_fan_cleaning: bool
    def __init__(self, set_temperature: _Optional[float] = ..., set_one_shot_mode: bool = ..., start_fan_cleaning: bool = ...) -> None: ...

class SEN6X_config(_message.Message):
    __slots__ = ["factory_reset", "set_altitude", "set_ambient_pressure", "set_asc", "set_one_shot_mode", "set_target_co2_conc", "set_temperature", "start_fan_cleaning"]
    FACTORY_RESET_FIELD_NUMBER: _ClassVar[int]
    SET_ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SET_AMBIENT_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    SET_ASC_FIELD_NUMBER: _ClassVar[int]
    SET_ONE_SHOT_MODE_FIELD_NUMBER: _ClassVar[int]
    SET_TARGET_CO2_CONC_FIELD_NUMBER: _ClassVar[int]
    SET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    START_FAN_CLEANING_FIELD_NUMBER: _ClassVar[int]
    factory_reset: bool
    set_altitude: int
    set_ambient_pressure: int
    set_asc: bool
    set_one_shot_mode: bool
    set_target_co2_conc: int
    set_temperature: float
    start_fan_cleaning: bool
    def __init__(self, set_temperature: _Optional[float] = ..., set_one_shot_mode: bool = ..., start_fan_cleaning: bool = ..., set_asc: bool = ..., set_target_co2_conc: _Optional[int] = ..., set_altitude: _Optional[int] = ..., set_ambient_pressure: _Optional[int] = ..., factory_reset: bool = ...) -> None: ...

class SHTXX_config(_message.Message):
    __slots__ = ["set_accuracy"]
    SET_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    set_accuracy: int
    def __init__(self, set_accuracy: _Optional[int] = ...) -> None: ...

class SensorConfig(_message.Message):
    __slots__ = ["as3935_config", "ds248x_config", "scd30_config", "scd4x_config", "sen5x_config", "sen6x_config", "shtxx_config"]
    AS3935_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DS248X_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SCD30_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SCD4X_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SEN5X_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SEN6X_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SHTXX_CONFIG_FIELD_NUMBER: _ClassVar[int]
    as3935_config: AS3935_config
    ds248x_config: DS248X_config
    scd30_config: SCD30_config
    scd4x_config: SCD4X_config
    sen5x_config: SEN5X_config
    sen6x_config: SEN6X_config
    shtxx_config: SHTXX_config
    def __init__(self, scd4x_config: _Optional[_Union[SCD4X_config, _Mapping]] = ..., sen5x_config: _Optional[_Union[SEN5X_config, _Mapping]] = ..., scd30_config: _Optional[_Union[SCD30_config, _Mapping]] = ..., shtxx_config: _Optional[_Union[SHTXX_config, _Mapping]] = ..., ds248x_config: _Optional[_Union[DS248X_config, _Mapping]] = ..., sen6x_config: _Optional[_Union[SEN6X_config, _Mapping]] = ..., as3935_config: _Optional[_Union[AS3935_config, _Mapping]] = ...) -> None: ...

class SharedContact(_message.Message):
    __slots__ = ["manually_verified", "node_num", "should_ignore", "user"]
    MANUALLY_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    NODE_NUM_FIELD_NUMBER: _ClassVar[int]
    SHOULD_IGNORE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    manually_verified: bool
    node_num: int
    should_ignore: bool
    user: _mesh_pb2.User
    def __init__(self, node_num: _Optional[int] = ..., user: _Optional[_Union[_mesh_pb2.User, _Mapping]] = ..., should_ignore: bool = ..., manually_verified: bool = ...) -> None: ...

class OTAMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
