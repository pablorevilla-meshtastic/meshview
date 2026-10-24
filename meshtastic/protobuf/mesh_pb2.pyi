from meshtastic.protobuf import channel_pb2 as _channel_pb2
from meshtastic.protobuf import config_pb2 as _config_pb2
from meshtastic.protobuf import device_ui_pb2 as _device_ui_pb2
from meshtastic.protobuf import field_metadata_pb2 as _field_metadata_pb2
from meshtastic.protobuf import module_config_pb2 as _module_config_pb2
from meshtastic.protobuf import portnums_pb2 as _portnums_pb2
from meshtastic.protobuf import telemetry_pb2 as _telemetry_pb2
from meshtastic.protobuf import xmodem_pb2 as _xmodem_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AMBIENTLIGHTING_CONFIG: ExcludedModules
ANDROID_SIM: HardwareModel
AUDIO_CONFIG: ExcludedModules
AXIOMETA_GENESIS_MINI: HardwareModel
BETAFPV_2400_TX: HardwareModel
BETAFPV_900_NANO_TX: HardwareModel
BLUETOOTH_CONFIG: ExcludedModules
BROWNOUT: CriticalErrorCode
BURNING_MAN: FirmwareEdition
CANARYONE: HardwareModel
CANNEDMSG_CONFIG: ExcludedModules
CCC: FirmwareEdition
CDEBYTE_EORA_S3: HardwareModel
CHATTER_2: HardwareModel
CROWPANEL: HardwareModel
CROWPANEL_P4: HardwareModel
DATA_PAYLOAD_LEN: Constants
DEFCON: FirmwareEdition
DESCRIPTOR: _descriptor.FileDescriptor
DETECTIONSENSOR_CONFIG: ExcludedModules
DIY_EDITION: FirmwareEdition
DIY_V1: HardwareModel
DRAGON_CON: FirmwareEdition
DR_DEV: HardwareModel
EBYTE_ESP32_S3: HardwareModel
ESP32_S3_PICO: HardwareModel
EXCLUDED_NONE: ExcludedModules
EXTNOTIF_CONFIG: ExcludedModules
FAB: FirmwareEdition
FLASH_CORRUPTION_RECOVERABLE: CriticalErrorCode
FLASH_CORRUPTION_UNRECOVERABLE: CriticalErrorCode
GENIEBLOCKS: HardwareModel
HAMVENTION: FirmwareEdition
HELTEC_CAPSULE_SENSOR_V3: HardwareModel
HELTEC_HRU_3601: HardwareModel
HELTEC_HT62: HardwareModel
HELTEC_MESH_NODE_T096: HardwareModel
HELTEC_MESH_NODE_T1: HardwareModel
HELTEC_MESH_NODE_T114: HardwareModel
HELTEC_MESH_POCKET: HardwareModel
HELTEC_MESH_POCKET_V2: HardwareModel
HELTEC_MESH_SOLAR: HardwareModel
HELTEC_MESH_TOWER_V2: HardwareModel
HELTEC_RC32: HardwareModel
HELTEC_RC52: HardwareModel
HELTEC_RCC6: HardwareModel
HELTEC_SENSOR_HUB: HardwareModel
HELTEC_V1: HardwareModel
HELTEC_V2_0: HardwareModel
HELTEC_V2_1: HardwareModel
HELTEC_V3: HardwareModel
HELTEC_V4: HardwareModel
HELTEC_V4_R8: HardwareModel
HELTEC_VISION_MASTER_E213: HardwareModel
HELTEC_VISION_MASTER_E290: HardwareModel
HELTEC_VISION_MASTER_T190: HardwareModel
HELTEC_WIRELESS_BRIDGE: HardwareModel
HELTEC_WIRELESS_PAPER: HardwareModel
HELTEC_WIRELESS_PAPER_V1_0: HardwareModel
HELTEC_WIRELESS_TRACKER: HardwareModel
HELTEC_WIRELESS_TRACKER_V1_0: HardwareModel
HELTEC_WIRELESS_TRACKER_V2: HardwareModel
HELTEC_WSL_V3: HardwareModel
INVALID_RADIO_SETTING: CriticalErrorCode
LILYGO_TBEAM_S3_CORE: HardwareModel
LINK_32: HardwareModel
LORA_RELAY_V1: HardwareModel
LORA_TYPE: HardwareModel
M5STACK: HardwareModel
M5STACK_C6L: HardwareModel
M5STACK_CARDPUTER_ADV: HardwareModel
M5STACK_CORE2: HardwareModel
M5STACK_COREBASIC: HardwareModel
M5STACK_CORES3: HardwareModel
M5STACK_RESERVED: HardwareModel
MAKERFABS_NOMAD_TERMINAL: HardwareModel
MAKERFABS_RESERVED: HardwareModel
MAKERFABS_TRACKER: HardwareModel
ME25LS01_4Y10TD: HardwareModel
MESHBEACON_CONFIG: ExcludedModules
MESHLINK: HardwareModel
MESHNOLOGY_W10: HardwareModel
MESHNOLOGY_W12: HardwareModel
MESHPAGER_X2: HardwareModel
MESHSTICK_1262: HardwareModel
MESH_TAB: HardwareModel
MESH_TRACKER_X1: HardwareModel
MINI_EPAPER_S3: HardwareModel
MQTT_CONFIG: ExcludedModules
MS24SF1: HardwareModel
MUZI_BASE: HardwareModel
MUZI_R1_NEO: HardwareModel
NANO_G1: HardwareModel
NANO_G1_EXPLORER: HardwareModel
NANO_G2_ULTRA: HardwareModel
NEIGHBORINFO_CONFIG: ExcludedModules
NETWORK_CONFIG: ExcludedModules
NODARA: HardwareModel
NOMADSTAR_METEOR_PRO: HardwareModel
NONE: CriticalErrorCode
NO_AXP192: CriticalErrorCode
NO_RADIO: CriticalErrorCode
NRF52840_PCA10059: HardwareModel
NRF52_PROMICRO_DIY: HardwareModel
NRF52_UNKNOWN: HardwareModel
OPEN_SAUCE: FirmwareEdition
PAXCOUNTER_CONFIG: ExcludedModules
PICOMPUTER_S3: HardwareModel
PORTDUINO: HardwareModel
PPR: HardwareModel
PRIVATE_HW: HardwareModel
RADIOMASTER_900_BANDIT: HardwareModel
RADIOMASTER_900_BANDIT_NANO: HardwareModel
RADIO_SPI_BUG: CriticalErrorCode
RAK11200: HardwareModel
RAK11310: HardwareModel
RAK2560: HardwareModel
RAK3172: HardwareModel
RAK3312: HardwareModel
RAK3401: HardwareModel
RAK4631: HardwareModel
RAK6421: HardwareModel
RANGETEST_CONFIG: ExcludedModules
REMOTEHARDWARE_CONFIG: ExcludedModules
ROUTASTIC: HardwareModel
RP2040_FEATHER_RFM95: HardwareModel
RP2040_LORA: HardwareModel
RPI_PICO: HardwareModel
RPI_PICO2: HardwareModel
SEEED_SOLAR_NODE: HardwareModel
SEEED_WIO_TRACKER_L1: HardwareModel
SEEED_WIO_TRACKER_L1_EINK: HardwareModel
SEEED_WIO_TRACKER_L1_PRO_1W: HardwareModel
SEEED_WIO_TRACKER_L2: HardwareModel
SEEED_XIAO_S3: HardwareModel
SENSECAP_INDICATOR: HardwareModel
SERIAL_CONFIG: ExcludedModules
SLEEP_ENTER_WAIT: CriticalErrorCode
SMART_CITIZEN: FirmwareEdition
STATION_G1: HardwareModel
STATION_G2: HardwareModel
STATION_G3: HardwareModel
STATUSMESSAGE_CONFIG: ExcludedModules
STOREFORWARD_CONFIG: ExcludedModules
SX1262_FAILURE: CriticalErrorCode
T5_S3_EPAPER_PRO: HardwareModel
TAK_CONFIG: ExcludedModules
TBEAM: HardwareModel
TBEAM_1_WATT: HardwareModel
TBEAM_BPF: HardwareModel
TBEAM_V0P7: HardwareModel
TDISPLAY_S3_PRO: HardwareModel
TD_LORAC: HardwareModel
TELEMETRY_CONFIG: ExcludedModules
THINKNODE_M1: HardwareModel
THINKNODE_M2: HardwareModel
THINKNODE_M3: HardwareModel
THINKNODE_M4: HardwareModel
THINKNODE_M5: HardwareModel
THINKNODE_M6: HardwareModel
THINKNODE_M7: HardwareModel
THINKNODE_M8: HardwareModel
THINKNODE_M9: HardwareModel
THINKNODE_MX: HardwareModel
TLORA_C6: HardwareModel
TLORA_T3_S3: HardwareModel
TLORA_V1: HardwareModel
TLORA_V1_1P3: HardwareModel
TLORA_V2: HardwareModel
TLORA_V2_1_1P6: HardwareModel
TLORA_V2_1_1P8: HardwareModel
TRACKER_T1000_E: HardwareModel
TRAFFICMANAGEMENT_CONFIG: ExcludedModules
TRANSMIT_FAILED: CriticalErrorCode
TWC_MESH_V4: HardwareModel
TX_WATCHDOG: CriticalErrorCode
T_CONNECT_PRO: HardwareModel
T_DECK: HardwareModel
T_DECK_PRO: HardwareModel
T_ECHO: HardwareModel
T_ECHO_CARD: HardwareModel
T_ECHO_LITE: HardwareModel
T_ECHO_PLUS: HardwareModel
T_ETH_ELITE: HardwareModel
T_IMPULSE_PLUS: HardwareModel
T_LORA_PAGER: HardwareModel
T_WATCH_S3: HardwareModel
T_WATCH_ULTRA: HardwareModel
UBLOX_UNIT_FAILED: CriticalErrorCode
UNPHONE: HardwareModel
UNSET: HardwareModel
UNSPECIFIED: CriticalErrorCode
VANILLA: FirmwareEdition
WIO_E5: HardwareModel
WIO_WM1110: HardwareModel
WIPHONE: HardwareModel
WISMESH_TAG: HardwareModel
WISMESH_TAP: HardwareModel
WISMESH_TAP_V2: HardwareModel
XIAO_NRF52_KIT: HardwareModel
ZERO: Constants

class BoundingBox(_message.Message):
    __slots__ = ["latitude_north_i", "latitude_south_i", "longitude_east_i", "longitude_west_i"]
    LATITUDE_NORTH_I_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_SOUTH_I_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_EAST_I_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_WEST_I_FIELD_NUMBER: _ClassVar[int]
    latitude_north_i: int
    latitude_south_i: int
    longitude_east_i: int
    longitude_west_i: int
    def __init__(self, longitude_west_i: _Optional[int] = ..., latitude_south_i: _Optional[int] = ..., longitude_east_i: _Optional[int] = ..., latitude_north_i: _Optional[int] = ...) -> None: ...

class ChunkedPayload(_message.Message):
    __slots__ = ["chunk_count", "chunk_index", "payload_chunk", "payload_id"]
    CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    chunk_count: int
    chunk_index: int
    payload_chunk: bytes
    payload_id: int
    def __init__(self, payload_id: _Optional[int] = ..., chunk_count: _Optional[int] = ..., chunk_index: _Optional[int] = ..., payload_chunk: _Optional[bytes] = ...) -> None: ...

class ChunkedPayloadResponse(_message.Message):
    __slots__ = ["accept_transfer", "payload_id", "request_transfer", "resend_chunks"]
    ACCEPT_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    RESEND_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    accept_transfer: bool
    payload_id: int
    request_transfer: bool
    resend_chunks: resend_chunks
    def __init__(self, payload_id: _Optional[int] = ..., request_transfer: bool = ..., accept_transfer: bool = ..., resend_chunks: _Optional[_Union[resend_chunks, _Mapping]] = ...) -> None: ...

class ClientNotification(_message.Message):
    __slots__ = ["duplicated_public_key", "key_verification_final", "key_verification_number_inform", "key_verification_number_request", "level", "low_entropy_key", "message", "reply_id", "time"]
    DUPLICATED_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_VERIFICATION_FINAL_FIELD_NUMBER: _ClassVar[int]
    KEY_VERIFICATION_NUMBER_INFORM_FIELD_NUMBER: _ClassVar[int]
    KEY_VERIFICATION_NUMBER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOW_ENTROPY_KEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REPLY_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    duplicated_public_key: DuplicatedPublicKey
    key_verification_final: KeyVerificationFinal
    key_verification_number_inform: KeyVerificationNumberInform
    key_verification_number_request: KeyVerificationNumberRequest
    level: LogRecord.Level
    low_entropy_key: LowEntropyKey
    message: str
    reply_id: int
    time: int
    def __init__(self, reply_id: _Optional[int] = ..., time: _Optional[int] = ..., level: _Optional[_Union[LogRecord.Level, str]] = ..., message: _Optional[str] = ..., key_verification_number_inform: _Optional[_Union[KeyVerificationNumberInform, _Mapping]] = ..., key_verification_number_request: _Optional[_Union[KeyVerificationNumberRequest, _Mapping]] = ..., key_verification_final: _Optional[_Union[KeyVerificationFinal, _Mapping]] = ..., duplicated_public_key: _Optional[_Union[DuplicatedPublicKey, _Mapping]] = ..., low_entropy_key: _Optional[_Union[LowEntropyKey, _Mapping]] = ...) -> None: ...

class Compressed(_message.Message):
    __slots__ = ["data", "portnum"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PORTNUM_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    portnum: _portnums_pb2.PortNum
    def __init__(self, portnum: _Optional[_Union[_portnums_pb2.PortNum, str]] = ..., data: _Optional[bytes] = ...) -> None: ...

class Data(_message.Message):
    __slots__ = ["bitfield", "dest", "emoji", "payload", "portnum", "reply_id", "request_id", "source", "want_response", "xeddsa_signature"]
    BITFIELD_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PORTNUM_FIELD_NUMBER: _ClassVar[int]
    REPLY_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    WANT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    XEDDSA_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    bitfield: int
    dest: int
    emoji: int
    payload: bytes
    portnum: _portnums_pb2.PortNum
    reply_id: int
    request_id: int
    source: int
    want_response: bool
    xeddsa_signature: bytes
    def __init__(self, portnum: _Optional[_Union[_portnums_pb2.PortNum, str]] = ..., payload: _Optional[bytes] = ..., want_response: bool = ..., dest: _Optional[int] = ..., source: _Optional[int] = ..., request_id: _Optional[int] = ..., reply_id: _Optional[int] = ..., emoji: _Optional[int] = ..., bitfield: _Optional[int] = ..., xeddsa_signature: _Optional[bytes] = ...) -> None: ...

class DeviceMetadata(_message.Message):
    __slots__ = ["canShutdown", "device_state_version", "excluded_modules", "firmware_version", "hasBluetooth", "hasEthernet", "hasPKC", "hasRemoteHardware", "hasWifi", "has_xeddsa", "hw_model", "position_flags", "role"]
    CANSHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_STATE_VERSION_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_MODULES_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    HASBLUETOOTH_FIELD_NUMBER: _ClassVar[int]
    HASETHERNET_FIELD_NUMBER: _ClassVar[int]
    HASPKC_FIELD_NUMBER: _ClassVar[int]
    HASREMOTEHARDWARE_FIELD_NUMBER: _ClassVar[int]
    HASWIFI_FIELD_NUMBER: _ClassVar[int]
    HAS_XEDDSA_FIELD_NUMBER: _ClassVar[int]
    HW_MODEL_FIELD_NUMBER: _ClassVar[int]
    POSITION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    canShutdown: bool
    device_state_version: int
    excluded_modules: int
    firmware_version: str
    hasBluetooth: bool
    hasEthernet: bool
    hasPKC: bool
    hasRemoteHardware: bool
    hasWifi: bool
    has_xeddsa: bool
    hw_model: HardwareModel
    position_flags: int
    role: _config_pb2.Config.DeviceConfig.Role
    def __init__(self, firmware_version: _Optional[str] = ..., device_state_version: _Optional[int] = ..., canShutdown: bool = ..., hasWifi: bool = ..., hasBluetooth: bool = ..., hasEthernet: bool = ..., role: _Optional[_Union[_config_pb2.Config.DeviceConfig.Role, str]] = ..., position_flags: _Optional[int] = ..., hw_model: _Optional[_Union[HardwareModel, str]] = ..., hasRemoteHardware: bool = ..., hasPKC: bool = ..., excluded_modules: _Optional[int] = ..., has_xeddsa: bool = ...) -> None: ...

class DuplicatedPublicKey(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class FileInfo(_message.Message):
    __slots__ = ["file_name", "size_bytes"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    size_bytes: int
    def __init__(self, file_name: _Optional[str] = ..., size_bytes: _Optional[int] = ...) -> None: ...

class FromRadio(_message.Message):
    __slots__ = ["channel", "clientNotification", "config", "config_complete_id", "deviceuiConfig", "fileInfo", "id", "lockdown_status", "log_record", "metadata", "moduleConfig", "mqttClientProxyMessage", "my_info", "node_info", "packet", "queueStatus", "rebooted", "region_presets", "xmodemPacket"]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CLIENTNOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_COMPLETE_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEVICEUICONFIG_FIELD_NUMBER: _ClassVar[int]
    FILEINFO_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCKDOWN_STATUS_FIELD_NUMBER: _ClassVar[int]
    LOG_RECORD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    MODULECONFIG_FIELD_NUMBER: _ClassVar[int]
    MQTTCLIENTPROXYMESSAGE_FIELD_NUMBER: _ClassVar[int]
    MY_INFO_FIELD_NUMBER: _ClassVar[int]
    NODE_INFO_FIELD_NUMBER: _ClassVar[int]
    PACKET_FIELD_NUMBER: _ClassVar[int]
    QUEUESTATUS_FIELD_NUMBER: _ClassVar[int]
    REBOOTED_FIELD_NUMBER: _ClassVar[int]
    REGION_PRESETS_FIELD_NUMBER: _ClassVar[int]
    XMODEMPACKET_FIELD_NUMBER: _ClassVar[int]
    channel: _channel_pb2.Channel
    clientNotification: ClientNotification
    config: _config_pb2.Config
    config_complete_id: int
    deviceuiConfig: _device_ui_pb2.DeviceUIConfig
    fileInfo: FileInfo
    id: int
    lockdown_status: LockdownStatus
    log_record: LogRecord
    metadata: DeviceMetadata
    moduleConfig: _module_config_pb2.ModuleConfig
    mqttClientProxyMessage: MqttClientProxyMessage
    my_info: MyNodeInfo
    node_info: NodeInfo
    packet: MeshPacket
    queueStatus: QueueStatus
    rebooted: bool
    region_presets: LoRaRegionPresetMap
    xmodemPacket: _xmodem_pb2.XModem
    def __init__(self, id: _Optional[int] = ..., packet: _Optional[_Union[MeshPacket, _Mapping]] = ..., my_info: _Optional[_Union[MyNodeInfo, _Mapping]] = ..., node_info: _Optional[_Union[NodeInfo, _Mapping]] = ..., config: _Optional[_Union[_config_pb2.Config, _Mapping]] = ..., log_record: _Optional[_Union[LogRecord, _Mapping]] = ..., config_complete_id: _Optional[int] = ..., rebooted: bool = ..., moduleConfig: _Optional[_Union[_module_config_pb2.ModuleConfig, _Mapping]] = ..., channel: _Optional[_Union[_channel_pb2.Channel, _Mapping]] = ..., queueStatus: _Optional[_Union[QueueStatus, _Mapping]] = ..., xmodemPacket: _Optional[_Union[_xmodem_pb2.XModem, _Mapping]] = ..., metadata: _Optional[_Union[DeviceMetadata, _Mapping]] = ..., mqttClientProxyMessage: _Optional[_Union[MqttClientProxyMessage, _Mapping]] = ..., fileInfo: _Optional[_Union[FileInfo, _Mapping]] = ..., clientNotification: _Optional[_Union[ClientNotification, _Mapping]] = ..., deviceuiConfig: _Optional[_Union[_device_ui_pb2.DeviceUIConfig, _Mapping]] = ..., lockdown_status: _Optional[_Union[LockdownStatus, _Mapping]] = ..., region_presets: _Optional[_Union[LoRaRegionPresetMap, _Mapping]] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ["nonce"]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    nonce: int
    def __init__(self, nonce: _Optional[int] = ...) -> None: ...

class KeyVerification(_message.Message):
    __slots__ = ["hash1", "hash2", "nonce"]
    HASH1_FIELD_NUMBER: _ClassVar[int]
    HASH2_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    hash1: bytes
    hash2: bytes
    nonce: int
    def __init__(self, nonce: _Optional[int] = ..., hash1: _Optional[bytes] = ..., hash2: _Optional[bytes] = ...) -> None: ...

class KeyVerificationFinal(_message.Message):
    __slots__ = ["isSender", "nonce", "remote_longname", "verification_characters"]
    ISSENDER_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    REMOTE_LONGNAME_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_CHARACTERS_FIELD_NUMBER: _ClassVar[int]
    isSender: bool
    nonce: int
    remote_longname: str
    verification_characters: str
    def __init__(self, nonce: _Optional[int] = ..., remote_longname: _Optional[str] = ..., isSender: bool = ..., verification_characters: _Optional[str] = ...) -> None: ...

class KeyVerificationNumberInform(_message.Message):
    __slots__ = ["nonce", "remote_longname", "security_number"]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    REMOTE_LONGNAME_FIELD_NUMBER: _ClassVar[int]
    SECURITY_NUMBER_FIELD_NUMBER: _ClassVar[int]
    nonce: int
    remote_longname: str
    security_number: int
    def __init__(self, nonce: _Optional[int] = ..., remote_longname: _Optional[str] = ..., security_number: _Optional[int] = ...) -> None: ...

class KeyVerificationNumberRequest(_message.Message):
    __slots__ = ["nonce", "remote_longname"]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    REMOTE_LONGNAME_FIELD_NUMBER: _ClassVar[int]
    nonce: int
    remote_longname: str
    def __init__(self, nonce: _Optional[int] = ..., remote_longname: _Optional[str] = ...) -> None: ...

class LoRaPresetGroup(_message.Message):
    __slots__ = ["default_preset", "licensed_only", "presets"]
    DEFAULT_PRESET_FIELD_NUMBER: _ClassVar[int]
    LICENSED_ONLY_FIELD_NUMBER: _ClassVar[int]
    PRESETS_FIELD_NUMBER: _ClassVar[int]
    default_preset: _config_pb2.Config.LoRaConfig.ModemPreset
    licensed_only: bool
    presets: _containers.RepeatedScalarFieldContainer[_config_pb2.Config.LoRaConfig.ModemPreset]
    def __init__(self, presets: _Optional[_Iterable[_Union[_config_pb2.Config.LoRaConfig.ModemPreset, str]]] = ..., default_preset: _Optional[_Union[_config_pb2.Config.LoRaConfig.ModemPreset, str]] = ..., licensed_only: bool = ...) -> None: ...

class LoRaRegionPresetMap(_message.Message):
    __slots__ = ["groups", "region_groups"]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    REGION_GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[LoRaPresetGroup]
    region_groups: _containers.RepeatedCompositeFieldContainer[LoRaRegionPresets]
    def __init__(self, groups: _Optional[_Iterable[_Union[LoRaPresetGroup, _Mapping]]] = ..., region_groups: _Optional[_Iterable[_Union[LoRaRegionPresets, _Mapping]]] = ...) -> None: ...

class LoRaRegionPresets(_message.Message):
    __slots__ = ["group_index", "region"]
    GROUP_INDEX_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    group_index: int
    region: _config_pb2.Config.LoRaConfig.RegionCode
    def __init__(self, region: _Optional[_Union[_config_pb2.Config.LoRaConfig.RegionCode, str]] = ..., group_index: _Optional[int] = ...) -> None: ...

class LockdownStatus(_message.Message):
    __slots__ = ["backoff_seconds", "boots_remaining", "lock_reason", "state", "valid_until_epoch"]
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BACKOFF_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BOOTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DISABLED: LockdownStatus.State
    LOCKED: LockdownStatus.State
    LOCK_REASON_FIELD_NUMBER: _ClassVar[int]
    NEEDS_PROVISION: LockdownStatus.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_UNSPECIFIED: LockdownStatus.State
    UNLOCKED: LockdownStatus.State
    UNLOCK_FAILED: LockdownStatus.State
    VALID_UNTIL_EPOCH_FIELD_NUMBER: _ClassVar[int]
    backoff_seconds: int
    boots_remaining: int
    lock_reason: str
    state: LockdownStatus.State
    valid_until_epoch: int
    def __init__(self, state: _Optional[_Union[LockdownStatus.State, str]] = ..., lock_reason: _Optional[str] = ..., boots_remaining: _Optional[int] = ..., valid_until_epoch: _Optional[int] = ..., backoff_seconds: _Optional[int] = ...) -> None: ...

class LogRecord(_message.Message):
    __slots__ = ["level", "message", "source", "time"]
    class Level(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CRITICAL: LogRecord.Level
    DEBUG: LogRecord.Level
    ERROR: LogRecord.Level
    INFO: LogRecord.Level
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TRACE: LogRecord.Level
    UNSET: LogRecord.Level
    WARNING: LogRecord.Level
    level: LogRecord.Level
    message: str
    source: str
    time: int
    def __init__(self, message: _Optional[str] = ..., time: _Optional[int] = ..., source: _Optional[str] = ..., level: _Optional[_Union[LogRecord.Level, str]] = ...) -> None: ...

class LowEntropyKey(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MeshPacket(_message.Message):
    __slots__ = ["ack_proof_status", "channel", "decoded", "delayed", "encrypted", "hop_limit", "hop_start", "id", "next_hop", "pki_encrypted", "priority", "public_key", "relay_node", "rx_rssi", "rx_snr", "rx_time", "slot_parity", "to", "transport_mechanism", "tx_after", "via_mqtt", "want_ack", "xeddsa_signed"]
    class AckProofStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Delayed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SlotParity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class TransportMechanism(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACK: MeshPacket.Priority
    ACK_PROOF_ABSENT: MeshPacket.AckProofStatus
    ACK_PROOF_INVALID: MeshPacket.AckProofStatus
    ACK_PROOF_NO_KEY: MeshPacket.AckProofStatus
    ACK_PROOF_STATUS_FIELD_NUMBER: _ClassVar[int]
    ACK_PROOF_VALID: MeshPacket.AckProofStatus
    ALERT: MeshPacket.Priority
    BACKGROUND: MeshPacket.Priority
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DECODED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT: MeshPacket.Priority
    DELAYED_BROADCAST: MeshPacket.Delayed
    DELAYED_DIRECT: MeshPacket.Delayed
    DELAYED_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    HIGH: MeshPacket.Priority
    HOP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    HOP_START_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAX: MeshPacket.Priority
    MIN: MeshPacket.Priority
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    NO_DELAY: MeshPacket.Delayed
    PKI_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    RELAY_NODE_FIELD_NUMBER: _ClassVar[int]
    RELIABLE: MeshPacket.Priority
    RESPONSE: MeshPacket.Priority
    RX_RSSI_FIELD_NUMBER: _ClassVar[int]
    RX_SNR_FIELD_NUMBER: _ClassVar[int]
    RX_TIME_FIELD_NUMBER: _ClassVar[int]
    SLOT_PARITY_EVEN: MeshPacket.SlotParity
    SLOT_PARITY_FIELD_NUMBER: _ClassVar[int]
    SLOT_PARITY_ODD: MeshPacket.SlotParity
    SLOT_PARITY_UNSET: MeshPacket.SlotParity
    TO_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_API: MeshPacket.TransportMechanism
    TRANSPORT_INTERNAL: MeshPacket.TransportMechanism
    TRANSPORT_LORA: MeshPacket.TransportMechanism
    TRANSPORT_LORA_ALT1: MeshPacket.TransportMechanism
    TRANSPORT_LORA_ALT2: MeshPacket.TransportMechanism
    TRANSPORT_LORA_ALT3: MeshPacket.TransportMechanism
    TRANSPORT_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_MQTT: MeshPacket.TransportMechanism
    TRANSPORT_MULTICAST_UDP: MeshPacket.TransportMechanism
    TRANSPORT_UNICAST_UDP: MeshPacket.TransportMechanism
    TX_AFTER_FIELD_NUMBER: _ClassVar[int]
    UNSET: MeshPacket.Priority
    VIA_MQTT_FIELD_NUMBER: _ClassVar[int]
    WANT_ACK_FIELD_NUMBER: _ClassVar[int]
    XEDDSA_SIGNED_FIELD_NUMBER: _ClassVar[int]
    ack_proof_status: MeshPacket.AckProofStatus
    channel: int
    decoded: Data
    delayed: MeshPacket.Delayed
    encrypted: bytes
    hop_limit: int
    hop_start: int
    id: int
    next_hop: int
    pki_encrypted: bool
    priority: MeshPacket.Priority
    public_key: bytes
    relay_node: int
    rx_rssi: int
    rx_snr: float
    rx_time: int
    slot_parity: MeshPacket.SlotParity
    to: int
    transport_mechanism: MeshPacket.TransportMechanism
    tx_after: int
    via_mqtt: bool
    want_ack: bool
    xeddsa_signed: bool
    def __init__(self, to: _Optional[int] = ..., channel: _Optional[int] = ..., decoded: _Optional[_Union[Data, _Mapping]] = ..., encrypted: _Optional[bytes] = ..., id: _Optional[int] = ..., rx_time: _Optional[int] = ..., rx_snr: _Optional[float] = ..., hop_limit: _Optional[int] = ..., want_ack: bool = ..., priority: _Optional[_Union[MeshPacket.Priority, str]] = ..., rx_rssi: _Optional[int] = ..., delayed: _Optional[_Union[MeshPacket.Delayed, str]] = ..., via_mqtt: bool = ..., hop_start: _Optional[int] = ..., public_key: _Optional[bytes] = ..., pki_encrypted: bool = ..., next_hop: _Optional[int] = ..., relay_node: _Optional[int] = ..., tx_after: _Optional[int] = ..., transport_mechanism: _Optional[_Union[MeshPacket.TransportMechanism, str]] = ..., xeddsa_signed: bool = ..., ack_proof_status: _Optional[_Union[MeshPacket.AckProofStatus, str]] = ..., slot_parity: _Optional[_Union[MeshPacket.SlotParity, str]] = ..., **kwargs) -> None: ...

class MqttClientProxyMessage(_message.Message):
    __slots__ = ["data", "retained", "text", "topic"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RETAINED_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    retained: bool
    text: str
    topic: str
    def __init__(self, topic: _Optional[str] = ..., data: _Optional[bytes] = ..., text: _Optional[str] = ..., retained: bool = ...) -> None: ...

class MyNodeInfo(_message.Message):
    __slots__ = ["device_id", "firmware_edition", "min_app_version", "my_node_num", "nodedb_count", "pio_env", "reboot_count"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_EDITION_FIELD_NUMBER: _ClassVar[int]
    MIN_APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    MY_NODE_NUM_FIELD_NUMBER: _ClassVar[int]
    NODEDB_COUNT_FIELD_NUMBER: _ClassVar[int]
    PIO_ENV_FIELD_NUMBER: _ClassVar[int]
    REBOOT_COUNT_FIELD_NUMBER: _ClassVar[int]
    device_id: bytes
    firmware_edition: FirmwareEdition
    min_app_version: int
    my_node_num: int
    nodedb_count: int
    pio_env: str
    reboot_count: int
    def __init__(self, my_node_num: _Optional[int] = ..., reboot_count: _Optional[int] = ..., min_app_version: _Optional[int] = ..., device_id: _Optional[bytes] = ..., pio_env: _Optional[str] = ..., firmware_edition: _Optional[_Union[FirmwareEdition, str]] = ..., nodedb_count: _Optional[int] = ...) -> None: ...

class Neighbor(_message.Message):
    __slots__ = ["last_rx_time", "node_broadcast_interval_secs", "node_id", "snr"]
    LAST_RX_TIME_FIELD_NUMBER: _ClassVar[int]
    NODE_BROADCAST_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    last_rx_time: int
    node_broadcast_interval_secs: int
    node_id: int
    snr: float
    def __init__(self, node_id: _Optional[int] = ..., snr: _Optional[float] = ..., last_rx_time: _Optional[int] = ..., node_broadcast_interval_secs: _Optional[int] = ...) -> None: ...

class NeighborInfo(_message.Message):
    __slots__ = ["last_sent_by_id", "neighbors", "node_broadcast_interval_secs", "node_id"]
    LAST_SENT_BY_ID_FIELD_NUMBER: _ClassVar[int]
    NEIGHBORS_FIELD_NUMBER: _ClassVar[int]
    NODE_BROADCAST_INTERVAL_SECS_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    last_sent_by_id: int
    neighbors: _containers.RepeatedCompositeFieldContainer[Neighbor]
    node_broadcast_interval_secs: int
    node_id: int
    def __init__(self, node_id: _Optional[int] = ..., last_sent_by_id: _Optional[int] = ..., node_broadcast_interval_secs: _Optional[int] = ..., neighbors: _Optional[_Iterable[_Union[Neighbor, _Mapping]]] = ...) -> None: ...

class NodeInfo(_message.Message):
    __slots__ = ["channel", "device_metrics", "has_xeddsa_signed", "heard_on_current_lora", "hops_away", "is_favorite", "is_ignored", "is_key_manually_verified", "is_muted", "last_heard", "num", "position", "snr", "user", "via_mqtt"]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_METRICS_FIELD_NUMBER: _ClassVar[int]
    HAS_XEDDSA_SIGNED_FIELD_NUMBER: _ClassVar[int]
    HEARD_ON_CURRENT_LORA_FIELD_NUMBER: _ClassVar[int]
    HOPS_AWAY_FIELD_NUMBER: _ClassVar[int]
    IS_FAVORITE_FIELD_NUMBER: _ClassVar[int]
    IS_IGNORED_FIELD_NUMBER: _ClassVar[int]
    IS_KEY_MANUALLY_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    IS_MUTED_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARD_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    VIA_MQTT_FIELD_NUMBER: _ClassVar[int]
    channel: int
    device_metrics: _telemetry_pb2.DeviceMetrics
    has_xeddsa_signed: bool
    heard_on_current_lora: bool
    hops_away: int
    is_favorite: bool
    is_ignored: bool
    is_key_manually_verified: bool
    is_muted: bool
    last_heard: int
    num: int
    position: Position
    snr: float
    user: User
    via_mqtt: bool
    def __init__(self, num: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ..., position: _Optional[_Union[Position, _Mapping]] = ..., snr: _Optional[float] = ..., last_heard: _Optional[int] = ..., device_metrics: _Optional[_Union[_telemetry_pb2.DeviceMetrics, _Mapping]] = ..., channel: _Optional[int] = ..., via_mqtt: bool = ..., hops_away: _Optional[int] = ..., is_favorite: bool = ..., is_ignored: bool = ..., is_key_manually_verified: bool = ..., is_muted: bool = ..., has_xeddsa_signed: bool = ..., heard_on_current_lora: bool = ...) -> None: ...

class NodeRemoteHardwarePin(_message.Message):
    __slots__ = ["node_num", "pin"]
    NODE_NUM_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    node_num: int
    pin: _module_config_pb2.RemoteHardwarePin
    def __init__(self, node_num: _Optional[int] = ..., pin: _Optional[_Union[_module_config_pb2.RemoteHardwarePin, _Mapping]] = ...) -> None: ...

class Position(_message.Message):
    __slots__ = ["HDOP", "PDOP", "VDOP", "altitude", "altitude_geoidal_separation", "altitude_hae", "altitude_source", "fix_quality", "fix_type", "gps_accuracy", "ground_speed", "ground_track", "latitude_i", "location_source", "longitude_i", "next_update", "precision_bits", "sats_in_view", "sensor_id", "seq_number", "time", "timestamp", "timestamp_millis_adjust"]
    class AltSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class LocSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_GEOIDAL_SEPARATION_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_HAE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ALT_BAROMETRIC: Position.AltSource
    ALT_EXTERNAL: Position.AltSource
    ALT_INTERNAL: Position.AltSource
    ALT_MANUAL: Position.AltSource
    ALT_UNSET: Position.AltSource
    FIX_QUALITY_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    GPS_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    GROUND_SPEED_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRACK_FIELD_NUMBER: _ClassVar[int]
    HDOP: int
    HDOP_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_I_FIELD_NUMBER: _ClassVar[int]
    LOCATION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LOC_EXTERNAL: Position.LocSource
    LOC_INTERNAL: Position.LocSource
    LOC_MANUAL: Position.LocSource
    LOC_UNSET: Position.LocSource
    LONGITUDE_I_FIELD_NUMBER: _ClassVar[int]
    NEXT_UPDATE_FIELD_NUMBER: _ClassVar[int]
    PDOP: int
    PDOP_FIELD_NUMBER: _ClassVar[int]
    PRECISION_BITS_FIELD_NUMBER: _ClassVar[int]
    SATS_IN_VIEW_FIELD_NUMBER: _ClassVar[int]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MILLIS_ADJUST_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    VDOP: int
    VDOP_FIELD_NUMBER: _ClassVar[int]
    altitude: int
    altitude_geoidal_separation: int
    altitude_hae: int
    altitude_source: Position.AltSource
    fix_quality: int
    fix_type: int
    gps_accuracy: int
    ground_speed: int
    ground_track: int
    latitude_i: int
    location_source: Position.LocSource
    longitude_i: int
    next_update: int
    precision_bits: int
    sats_in_view: int
    sensor_id: int
    seq_number: int
    time: int
    timestamp: int
    timestamp_millis_adjust: int
    def __init__(self, latitude_i: _Optional[int] = ..., longitude_i: _Optional[int] = ..., altitude: _Optional[int] = ..., time: _Optional[int] = ..., location_source: _Optional[_Union[Position.LocSource, str]] = ..., altitude_source: _Optional[_Union[Position.AltSource, str]] = ..., timestamp: _Optional[int] = ..., timestamp_millis_adjust: _Optional[int] = ..., altitude_hae: _Optional[int] = ..., altitude_geoidal_separation: _Optional[int] = ..., PDOP: _Optional[int] = ..., HDOP: _Optional[int] = ..., VDOP: _Optional[int] = ..., gps_accuracy: _Optional[int] = ..., ground_speed: _Optional[int] = ..., ground_track: _Optional[int] = ..., fix_quality: _Optional[int] = ..., fix_type: _Optional[int] = ..., sats_in_view: _Optional[int] = ..., sensor_id: _Optional[int] = ..., next_update: _Optional[int] = ..., seq_number: _Optional[int] = ..., precision_bits: _Optional[int] = ...) -> None: ...

class QueueStatus(_message.Message):
    __slots__ = ["free", "maxlen", "mesh_packet_id", "res"]
    FREE_FIELD_NUMBER: _ClassVar[int]
    MAXLEN_FIELD_NUMBER: _ClassVar[int]
    MESH_PACKET_ID_FIELD_NUMBER: _ClassVar[int]
    RES_FIELD_NUMBER: _ClassVar[int]
    free: int
    maxlen: int
    mesh_packet_id: int
    res: int
    def __init__(self, res: _Optional[int] = ..., free: _Optional[int] = ..., maxlen: _Optional[int] = ..., mesh_packet_id: _Optional[int] = ...) -> None: ...

class RemoteShell(_message.Message):
    __slots__ = ["ack_seq", "cols", "flags", "last_rx_seq", "last_tx_seq", "op", "payload", "rows", "seq", "session_id"]
    class OpCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACK: RemoteShell.OpCode
    ACK_SEQ_FIELD_NUMBER: _ClassVar[int]
    CLOSE: RemoteShell.OpCode
    CLOSED: RemoteShell.OpCode
    COLS_FIELD_NUMBER: _ClassVar[int]
    ERROR: RemoteShell.OpCode
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    INPUT: RemoteShell.OpCode
    LAST_RX_SEQ_FIELD_NUMBER: _ClassVar[int]
    LAST_TX_SEQ_FIELD_NUMBER: _ClassVar[int]
    OPEN: RemoteShell.OpCode
    OPEN_OK: RemoteShell.OpCode
    OP_FIELD_NUMBER: _ClassVar[int]
    OP_UNSET: RemoteShell.OpCode
    OUTPUT: RemoteShell.OpCode
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PING: RemoteShell.OpCode
    PONG: RemoteShell.OpCode
    RESIZE: RemoteShell.OpCode
    ROWS_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    ack_seq: int
    cols: int
    flags: int
    last_rx_seq: int
    last_tx_seq: int
    op: RemoteShell.OpCode
    payload: bytes
    rows: int
    seq: int
    session_id: int
    def __init__(self, op: _Optional[_Union[RemoteShell.OpCode, str]] = ..., session_id: _Optional[int] = ..., seq: _Optional[int] = ..., ack_seq: _Optional[int] = ..., payload: _Optional[bytes] = ..., cols: _Optional[int] = ..., rows: _Optional[int] = ..., flags: _Optional[int] = ..., last_tx_seq: _Optional[int] = ..., last_rx_seq: _Optional[int] = ...) -> None: ...

class RouteDiscovery(_message.Message):
    __slots__ = ["route", "route_back", "snr_back", "snr_towards"]
    ROUTE_BACK_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    SNR_BACK_FIELD_NUMBER: _ClassVar[int]
    SNR_TOWARDS_FIELD_NUMBER: _ClassVar[int]
    route: _containers.RepeatedScalarFieldContainer[int]
    route_back: _containers.RepeatedScalarFieldContainer[int]
    snr_back: _containers.RepeatedScalarFieldContainer[int]
    snr_towards: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, route: _Optional[_Iterable[int]] = ..., snr_towards: _Optional[_Iterable[int]] = ..., route_back: _Optional[_Iterable[int]] = ..., snr_back: _Optional[_Iterable[int]] = ...) -> None: ...

class Routing(_message.Message):
    __slots__ = ["ack_proof", "error_reason", "route_reply", "route_request"]
    class Error(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACK_PROOF_FIELD_NUMBER: _ClassVar[int]
    ADMIN_BAD_SESSION_KEY: Routing.Error
    ADMIN_PUBLIC_KEY_UNAUTHORIZED: Routing.Error
    BAD_REQUEST: Routing.Error
    DUTY_CYCLE_LIMIT: Routing.Error
    ERROR_REASON_FIELD_NUMBER: _ClassVar[int]
    GOT_NAK: Routing.Error
    MAX_RETRANSMIT: Routing.Error
    NONE: Routing.Error
    NOT_AUTHORIZED: Routing.Error
    NO_CHANNEL: Routing.Error
    NO_INTERFACE: Routing.Error
    NO_RESPONSE: Routing.Error
    NO_ROUTE: Routing.Error
    PKI_FAILED: Routing.Error
    PKI_SEND_FAIL_PUBLIC_KEY: Routing.Error
    PKI_UNKNOWN_PUBKEY: Routing.Error
    RATE_LIMIT_EXCEEDED: Routing.Error
    ROUTE_REPLY_FIELD_NUMBER: _ClassVar[int]
    ROUTE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT: Routing.Error
    TOO_LARGE: Routing.Error
    ack_proof: bytes
    error_reason: Routing.Error
    route_reply: RouteDiscovery
    route_request: RouteDiscovery
    def __init__(self, route_request: _Optional[_Union[RouteDiscovery, _Mapping]] = ..., route_reply: _Optional[_Union[RouteDiscovery, _Mapping]] = ..., error_reason: _Optional[_Union[Routing.Error, str]] = ..., ack_proof: _Optional[bytes] = ...) -> None: ...

class StatusMessage(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class StoreForwardPlusPlus(_message.Message):
    __slots__ = ["chain_count", "commit_hash", "encapsulated_from", "encapsulated_id", "encapsulated_rxtime", "encapsulated_to", "message", "message_hash", "root_hash", "sfpp_message_type"]
    class SFPP_message_type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CANON_ANNOUNCE: StoreForwardPlusPlus.SFPP_message_type
    CHAIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHAIN_QUERY: StoreForwardPlusPlus.SFPP_message_type
    COMMIT_HASH_FIELD_NUMBER: _ClassVar[int]
    ENCAPSULATED_FROM_FIELD_NUMBER: _ClassVar[int]
    ENCAPSULATED_ID_FIELD_NUMBER: _ClassVar[int]
    ENCAPSULATED_RXTIME_FIELD_NUMBER: _ClassVar[int]
    ENCAPSULATED_TO_FIELD_NUMBER: _ClassVar[int]
    LINK_PROVIDE: StoreForwardPlusPlus.SFPP_message_type
    LINK_PROVIDE_FIRSTHALF: StoreForwardPlusPlus.SFPP_message_type
    LINK_PROVIDE_SECONDHALF: StoreForwardPlusPlus.SFPP_message_type
    LINK_REQUEST: StoreForwardPlusPlus.SFPP_message_type
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_HASH_FIELD_NUMBER: _ClassVar[int]
    ROOT_HASH_FIELD_NUMBER: _ClassVar[int]
    SFPP_MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    chain_count: int
    commit_hash: bytes
    encapsulated_from: int
    encapsulated_id: int
    encapsulated_rxtime: int
    encapsulated_to: int
    message: bytes
    message_hash: bytes
    root_hash: bytes
    sfpp_message_type: StoreForwardPlusPlus.SFPP_message_type
    def __init__(self, sfpp_message_type: _Optional[_Union[StoreForwardPlusPlus.SFPP_message_type, str]] = ..., message_hash: _Optional[bytes] = ..., commit_hash: _Optional[bytes] = ..., root_hash: _Optional[bytes] = ..., message: _Optional[bytes] = ..., encapsulated_id: _Optional[int] = ..., encapsulated_to: _Optional[int] = ..., encapsulated_from: _Optional[int] = ..., encapsulated_rxtime: _Optional[int] = ..., chain_count: _Optional[int] = ...) -> None: ...

class ToRadio(_message.Message):
    __slots__ = ["disconnect", "heartbeat", "mqttClientProxyMessage", "packet", "want_config_id", "xmodemPacket"]
    DISCONNECT_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    MQTTCLIENTPROXYMESSAGE_FIELD_NUMBER: _ClassVar[int]
    PACKET_FIELD_NUMBER: _ClassVar[int]
    WANT_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    XMODEMPACKET_FIELD_NUMBER: _ClassVar[int]
    disconnect: bool
    heartbeat: Heartbeat
    mqttClientProxyMessage: MqttClientProxyMessage
    packet: MeshPacket
    want_config_id: int
    xmodemPacket: _xmodem_pb2.XModem
    def __init__(self, packet: _Optional[_Union[MeshPacket, _Mapping]] = ..., want_config_id: _Optional[int] = ..., disconnect: bool = ..., xmodemPacket: _Optional[_Union[_xmodem_pb2.XModem, _Mapping]] = ..., mqttClientProxyMessage: _Optional[_Union[MqttClientProxyMessage, _Mapping]] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["hw_model", "id", "is_licensed", "is_unmessagable", "long_name", "macaddr", "public_key", "role", "short_name"]
    HW_MODEL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_LICENSED_FIELD_NUMBER: _ClassVar[int]
    IS_UNMESSAGABLE_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    MACADDR_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    hw_model: HardwareModel
    id: str
    is_licensed: bool
    is_unmessagable: bool
    long_name: str
    macaddr: bytes
    public_key: bytes
    role: _config_pb2.Config.DeviceConfig.Role
    short_name: str
    def __init__(self, id: _Optional[str] = ..., long_name: _Optional[str] = ..., short_name: _Optional[str] = ..., macaddr: _Optional[bytes] = ..., hw_model: _Optional[_Union[HardwareModel, str]] = ..., is_licensed: bool = ..., role: _Optional[_Union[_config_pb2.Config.DeviceConfig.Role, str]] = ..., public_key: _Optional[bytes] = ..., is_unmessagable: bool = ...) -> None: ...

class Waypoint(_message.Message):
    __slots__ = ["bounding_box", "description", "expire", "geofence_radius", "icon", "id", "latitude_i", "locked_to", "longitude_i", "name", "notify_favorites_only", "notify_on_enter", "notify_on_exit"]
    BOUNDING_BOX_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    GEOFENCE_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_I_FIELD_NUMBER: _ClassVar[int]
    LOCKED_TO_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_I_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_FAVORITES_ONLY_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_ON_ENTER_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_ON_EXIT_FIELD_NUMBER: _ClassVar[int]
    bounding_box: BoundingBox
    description: str
    expire: int
    geofence_radius: int
    icon: int
    id: int
    latitude_i: int
    locked_to: int
    longitude_i: int
    name: str
    notify_favorites_only: bool
    notify_on_enter: bool
    notify_on_exit: bool
    def __init__(self, id: _Optional[int] = ..., latitude_i: _Optional[int] = ..., longitude_i: _Optional[int] = ..., expire: _Optional[int] = ..., locked_to: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., icon: _Optional[int] = ..., geofence_radius: _Optional[int] = ..., bounding_box: _Optional[_Union[BoundingBox, _Mapping]] = ..., notify_on_enter: bool = ..., notify_on_exit: bool = ..., notify_favorites_only: bool = ...) -> None: ...

class resend_chunks(_message.Message):
    __slots__ = ["chunks"]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    chunks: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, chunks: _Optional[_Iterable[int]] = ...) -> None: ...

class HardwareModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Constants(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CriticalErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FirmwareEdition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ExcludedModules(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
