from meshtastic.protobuf import localonly_pb2 as _localonly_pb2
from meshtastic.protobuf import mesh_pb2 as _mesh_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceProfile(_message.Message):
    __slots__ = ["canned_messages", "channel_url", "config", "fixed_position", "is_licensed", "is_unmessagable", "long_name", "module_config", "ringtone", "short_name"]
    CANNED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_URL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    FIXED_POSITION_FIELD_NUMBER: _ClassVar[int]
    IS_LICENSED_FIELD_NUMBER: _ClassVar[int]
    IS_UNMESSAGABLE_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RINGTONE_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    canned_messages: str
    channel_url: str
    config: _localonly_pb2.LocalConfig
    fixed_position: _mesh_pb2.Position
    is_licensed: bool
    is_unmessagable: bool
    long_name: str
    module_config: _localonly_pb2.LocalModuleConfig
    ringtone: str
    short_name: str
    def __init__(self, long_name: _Optional[str] = ..., short_name: _Optional[str] = ..., channel_url: _Optional[str] = ..., config: _Optional[_Union[_localonly_pb2.LocalConfig, _Mapping]] = ..., module_config: _Optional[_Union[_localonly_pb2.LocalModuleConfig, _Mapping]] = ..., fixed_position: _Optional[_Union[_mesh_pb2.Position, _Mapping]] = ..., ringtone: _Optional[str] = ..., canned_messages: _Optional[str] = ..., is_unmessagable: bool = ..., is_licensed: bool = ...) -> None: ...
