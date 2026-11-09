from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
ENUM_VALUE_METADATA_FIELD_NUMBER: _ClassVar[int]
FIELD_METADATA_FIELD_NUMBER: _ClassVar[int]
enum_value_metadata: _descriptor.FieldDescriptor
field_metadata: _descriptor.FieldDescriptor

class FieldMetadata(_message.Message):
    __slots__ = ["admin_only", "deprecated", "deprecated_since", "description", "diy_only", "keywords", "label", "max_value", "min_value", "oem_fixed_gps", "since_firmware", "unit"]
    ADMIN_ONLY_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_SINCE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DIY_ONLY_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
    MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
    OEM_FIXED_GPS_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIRMWARE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    admin_only: bool
    deprecated: bool
    deprecated_since: str
    description: str
    diy_only: bool
    keywords: str
    label: str
    max_value: float
    min_value: float
    oem_fixed_gps: bool
    since_firmware: str
    unit: str
    def __init__(self, diy_only: bool = ..., admin_only: bool = ..., min_value: _Optional[float] = ..., max_value: _Optional[float] = ..., unit: _Optional[str] = ..., deprecated: bool = ..., label: _Optional[str] = ..., description: _Optional[str] = ..., keywords: _Optional[str] = ..., since_firmware: _Optional[str] = ..., deprecated_since: _Optional[str] = ..., oem_fixed_gps: bool = ...) -> None: ...
