from meshtastic.protobuf import deviceonly_pb2 as _deviceonly_pb2
from meshtastic.protobuf import telemetry_pb2 as _telemetry_pb2
from meshtastic.protobuf import nanopb_pb2 as _nanopb_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeDatabase_Legacy(_message.Message):
    __slots__ = ["nodes", "version"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[NodeInfoLite_Legacy]
    version: int
    def __init__(self, version: _Optional[int] = ..., nodes: _Optional[_Iterable[_Union[NodeInfoLite_Legacy, _Mapping]]] = ...) -> None: ...

class NodeInfoLite_Legacy(_message.Message):
    __slots__ = ["bitfield", "channel", "device_metrics", "hops_away", "is_favorite", "is_ignored", "last_heard", "next_hop", "num", "position", "snr", "user", "via_mqtt"]
    BITFIELD_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_METRICS_FIELD_NUMBER: _ClassVar[int]
    HOPS_AWAY_FIELD_NUMBER: _ClassVar[int]
    IS_FAVORITE_FIELD_NUMBER: _ClassVar[int]
    IS_IGNORED_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARD_FIELD_NUMBER: _ClassVar[int]
    NEXT_HOP_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    VIA_MQTT_FIELD_NUMBER: _ClassVar[int]
    bitfield: int
    channel: int
    device_metrics: _telemetry_pb2.DeviceMetrics
    hops_away: int
    is_favorite: bool
    is_ignored: bool
    last_heard: int
    next_hop: int
    num: int
    position: _deviceonly_pb2.PositionLite
    snr: float
    user: _deviceonly_pb2.UserLite
    via_mqtt: bool
    def __init__(self, num: _Optional[int] = ..., user: _Optional[_Union[_deviceonly_pb2.UserLite, _Mapping]] = ..., position: _Optional[_Union[_deviceonly_pb2.PositionLite, _Mapping]] = ..., snr: _Optional[float] = ..., last_heard: _Optional[int] = ..., device_metrics: _Optional[_Union[_telemetry_pb2.DeviceMetrics, _Mapping]] = ..., channel: _Optional[int] = ..., via_mqtt: bool = ..., hops_away: _Optional[int] = ..., is_favorite: bool = ..., is_ignored: bool = ..., next_hop: _Optional[int] = ..., bitfield: _Optional[int] = ...) -> None: ...
