from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(_message.Message):
    __slots__ = ["index", "role", "settings"]
    class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DISABLED: Channel.Role
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PRIMARY: Channel.Role
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SECONDARY: Channel.Role
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    index: int
    role: Channel.Role
    settings: ChannelSettings
    def __init__(self, index: _Optional[int] = ..., settings: _Optional[_Union[ChannelSettings, _Mapping]] = ..., role: _Optional[_Union[Channel.Role, str]] = ...) -> None: ...

class ChannelSettings(_message.Message):
    __slots__ = ["channel_num", "downlink_enabled", "id", "module_settings", "name", "psk", "uplink_enabled", "use_aead"]
    CHANNEL_NUM_FIELD_NUMBER: _ClassVar[int]
    DOWNLINK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PSK_FIELD_NUMBER: _ClassVar[int]
    UPLINK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    USE_AEAD_FIELD_NUMBER: _ClassVar[int]
    channel_num: int
    downlink_enabled: bool
    id: int
    module_settings: ModuleSettings
    name: str
    psk: bytes
    uplink_enabled: bool
    use_aead: bool
    def __init__(self, channel_num: _Optional[int] = ..., psk: _Optional[bytes] = ..., name: _Optional[str] = ..., id: _Optional[int] = ..., uplink_enabled: bool = ..., downlink_enabled: bool = ..., module_settings: _Optional[_Union[ModuleSettings, _Mapping]] = ..., use_aead: bool = ...) -> None: ...

class ModuleSettings(_message.Message):
    __slots__ = ["is_muted", "position_precision"]
    IS_MUTED_FIELD_NUMBER: _ClassVar[int]
    POSITION_PRECISION_FIELD_NUMBER: _ClassVar[int]
    is_muted: bool
    position_precision: int
    def __init__(self, position_precision: _Optional[int] = ..., is_muted: bool = ...) -> None: ...
