from meshtastic.protobuf import channel_pb2 as _channel_pb2
from meshtastic.protobuf import config_pb2 as _config_pb2
from meshtastic.protobuf import localonly_pb2 as _localonly_pb2
from meshtastic.protobuf import mesh_pb2 as _mesh_pb2
from meshtastic.protobuf import telemetry_pb2 as _telemetry_pb2
from meshtastic.protobuf import nanopb_pb2 as _nanopb_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BackupPreferences(_message.Message):
    __slots__ = ["channels", "config", "module_config", "owner", "timestamp", "version"]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    MODULE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    channels: ChannelFile
    config: _localonly_pb2.LocalConfig
    module_config: _localonly_pb2.LocalModuleConfig
    owner: _mesh_pb2.User
    timestamp: int
    version: int
    def __init__(self, version: _Optional[int] = ..., timestamp: _Optional[int] = ..., config: _Optional[_Union[_localonly_pb2.LocalConfig, _Mapping]] = ..., module_config: _Optional[_Union[_localonly_pb2.LocalModuleConfig, _Mapping]] = ..., channels: _Optional[_Union[ChannelFile, _Mapping]] = ..., owner: _Optional[_Union[_mesh_pb2.User, _Mapping]] = ...) -> None: ...

class ChannelFile(_message.Message):
    __slots__ = ["channels", "version"]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[_channel_pb2.Channel]
    version: int
    def __init__(self, channels: _Optional[_Iterable[_Union[_channel_pb2.Channel, _Mapping]]] = ..., version: _Optional[int] = ...) -> None: ...

class DeviceState(_message.Message):
    __slots__ = ["did_gps_reset", "my_node", "no_save", "node_remote_hardware_pins", "owner", "receive_queue", "rx_text_message", "rx_waypoint", "version"]
    DID_GPS_RESET_FIELD_NUMBER: _ClassVar[int]
    MY_NODE_FIELD_NUMBER: _ClassVar[int]
    NODE_REMOTE_HARDWARE_PINS_FIELD_NUMBER: _ClassVar[int]
    NO_SAVE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    RECEIVE_QUEUE_FIELD_NUMBER: _ClassVar[int]
    RX_TEXT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RX_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    did_gps_reset: bool
    my_node: _mesh_pb2.MyNodeInfo
    no_save: bool
    node_remote_hardware_pins: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.NodeRemoteHardwarePin]
    owner: _mesh_pb2.User
    receive_queue: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.MeshPacket]
    rx_text_message: _mesh_pb2.MeshPacket
    rx_waypoint: _mesh_pb2.MeshPacket
    version: int
    def __init__(self, my_node: _Optional[_Union[_mesh_pb2.MyNodeInfo, _Mapping]] = ..., owner: _Optional[_Union[_mesh_pb2.User, _Mapping]] = ..., receive_queue: _Optional[_Iterable[_Union[_mesh_pb2.MeshPacket, _Mapping]]] = ..., version: _Optional[int] = ..., rx_text_message: _Optional[_Union[_mesh_pb2.MeshPacket, _Mapping]] = ..., no_save: bool = ..., did_gps_reset: bool = ..., rx_waypoint: _Optional[_Union[_mesh_pb2.MeshPacket, _Mapping]] = ..., node_remote_hardware_pins: _Optional[_Iterable[_Union[_mesh_pb2.NodeRemoteHardwarePin, _Mapping]]] = ...) -> None: ...

class NodeDatabase(_message.Message):
    __slots__ = ["environment", "nodes", "positions", "status", "telemetry", "version"]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    environment: _containers.RepeatedCompositeFieldContainer[NodeEnvironmentEntry]
    nodes: _containers.RepeatedCompositeFieldContainer[NodeInfoLite]
    positions: _containers.RepeatedCompositeFieldContainer[NodePositionEntry]
    status: _containers.RepeatedCompositeFieldContainer[NodeStatusEntry]
    telemetry: _containers.RepeatedCompositeFieldContainer[NodeTelemetryEntry]
    version: int
    def __init__(self, version: _Optional[int] = ..., nodes: _Optional[_Iterable[_Union[NodeInfoLite, _Mapping]]] = ..., positions: _Optional[_Iterable[_Union[NodePositionEntry, _Mapping]]] = ..., telemetry: _Optional[_Iterable[_Union[NodeTelemetryEntry, _Mapping]]] = ..., status: _Optional[_Iterable[_Union[NodeStatusEntry, _Mapping]]] = ..., environment: _Optional[_Iterable[_Union[NodeEnvironmentEntry, _Mapping]]] = ...) -> None: ...

class NodeEnvironmentEntry(_message.Message):
    __slots__ = ["environment_metrics", "num"]
    ENVIRONMENT_METRICS_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    environment_metrics: _telemetry_pb2.EnvironmentMetrics
    num: int
    def __init__(self, num: _Optional[int] = ..., environment_metrics: _Optional[_Union[_telemetry_pb2.EnvironmentMetrics, _Mapping]] = ...) -> None: ...

class NodeInfoLite(_message.Message):
    __slots__ = ["bitfield", "channel", "hops_away", "hw_model", "last_heard", "long_name", "next_hop", "num", "public_key", "role", "short_name", "snr", "snr_q4"]
    BITFIELD_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    HOPS_AWAY_FIELD_NUMBER: _ClassVar[int]
    HW_MODEL_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARD_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    SNR_Q4_FIELD_NUMBER: _ClassVar[int]
    bitfield: int
    channel: int
    hops_away: int
    hw_model: _mesh_pb2.HardwareModel
    last_heard: int
    long_name: str
    next_hop: int
    num: int
    public_key: bytes
    role: _config_pb2.Config.DeviceConfig.Role
    short_name: str
    snr: float
    snr_q4: int
    def __init__(self, num: _Optional[int] = ..., snr: _Optional[float] = ..., last_heard: _Optional[int] = ..., channel: _Optional[int] = ..., hops_away: _Optional[int] = ..., next_hop: _Optional[int] = ..., bitfield: _Optional[int] = ..., long_name: _Optional[str] = ..., short_name: _Optional[str] = ..., hw_model: _Optional[_Union[_mesh_pb2.HardwareModel, str]] = ..., role: _Optional[_Union[_config_pb2.Config.DeviceConfig.Role, str]] = ..., public_key: _Optional[bytes] = ..., snr_q4: _Optional[int] = ...) -> None: ...

class NodePositionEntry(_message.Message):
    __slots__ = ["num", "position"]
    NUM_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    num: int
    position: PositionLite
    def __init__(self, num: _Optional[int] = ..., position: _Optional[_Union[PositionLite, _Mapping]] = ...) -> None: ...

class NodeStatusEntry(_message.Message):
    __slots__ = ["num", "status"]
    NUM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    num: int
    status: _mesh_pb2.StatusMessage
    def __init__(self, num: _Optional[int] = ..., status: _Optional[_Union[_mesh_pb2.StatusMessage, _Mapping]] = ...) -> None: ...

class NodeTelemetryEntry(_message.Message):
    __slots__ = ["device_metrics", "num"]
    DEVICE_METRICS_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    device_metrics: _telemetry_pb2.DeviceMetrics
    num: int
    def __init__(self, num: _Optional[int] = ..., device_metrics: _Optional[_Union[_telemetry_pb2.DeviceMetrics, _Mapping]] = ...) -> None: ...

class PositionLite(_message.Message):
    __slots__ = ["altitude", "latitude_i", "location_source", "longitude_i", "precision_bits", "time"]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_I_FIELD_NUMBER: _ClassVar[int]
    LOCATION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_I_FIELD_NUMBER: _ClassVar[int]
    PRECISION_BITS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    altitude: int
    latitude_i: int
    location_source: _mesh_pb2.Position.LocSource
    longitude_i: int
    precision_bits: int
    time: int
    def __init__(self, latitude_i: _Optional[int] = ..., longitude_i: _Optional[int] = ..., altitude: _Optional[int] = ..., time: _Optional[int] = ..., location_source: _Optional[_Union[_mesh_pb2.Position.LocSource, str]] = ..., precision_bits: _Optional[int] = ...) -> None: ...

class UserLite(_message.Message):
    __slots__ = ["hw_model", "is_licensed", "is_unmessagable", "long_name", "macaddr", "public_key", "role", "short_name"]
    HW_MODEL_FIELD_NUMBER: _ClassVar[int]
    IS_LICENSED_FIELD_NUMBER: _ClassVar[int]
    IS_UNMESSAGABLE_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    MACADDR_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    hw_model: _mesh_pb2.HardwareModel
    is_licensed: bool
    is_unmessagable: bool
    long_name: str
    macaddr: bytes
    public_key: bytes
    role: _config_pb2.Config.DeviceConfig.Role
    short_name: str
    def __init__(self, macaddr: _Optional[bytes] = ..., long_name: _Optional[str] = ..., short_name: _Optional[str] = ..., hw_model: _Optional[_Union[_mesh_pb2.HardwareModel, str]] = ..., is_licensed: bool = ..., role: _Optional[_Union[_config_pb2.Config.DeviceConfig.Role, str]] = ..., public_key: _Optional[bytes] = ..., is_unmessagable: bool = ...) -> None: ...
