from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DELETE: FileOperation
DESCRIPTOR: _descriptor.FileDescriptor
FILE_BUSY: FileStatus
FILE_IO_ERROR: FileStatus
FILE_NOT_A_FILE: FileStatus
FILE_NOT_FOUND: FileStatus
FILE_NO_CARD: FileStatus
FILE_OFFSET_CONFLICT: FileStatus
FILE_OK: FileStatus
FILE_UNSPECIFIED: FileStatus
GET: FileOperation
INTERDEVICE_VERSION_CURRENT: InterdeviceVersion
INTERDEVICE_VERSION_UNSPECIFIED: InterdeviceVersion
POST: FileOperation
PUT: FileOperation
SD_COMMAND_UNSPECIFIED: SdCommand
SD_EJECT: SdCommand
SD_FORMAT: SdCommand
SD_MOUNT: SdCommand

class DirectoryListing(_message.Message):
    __slots__ = ["directory", "filenames", "message", "offset", "status", "total_count"]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    FILENAMES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    directory: str
    filenames: _containers.RepeatedScalarFieldContainer[str]
    message: str
    offset: int
    status: FileStatus
    total_count: int
    def __init__(self, directory: _Optional[str] = ..., filenames: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[FileStatus, str]] = ..., message: _Optional[str] = ..., offset: _Optional[int] = ..., total_count: _Optional[int] = ...) -> None: ...

class FileTransfer(_message.Message):
    __slots__ = ["file_size", "filedata", "filepath", "length", "message", "offset", "operation", "status"]
    FILEDATA_FIELD_NUMBER: _ClassVar[int]
    FILEPATH_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    file_size: int
    filedata: bytes
    filepath: str
    length: int
    message: str
    offset: int
    operation: FileOperation
    status: FileStatus
    def __init__(self, operation: _Optional[_Union[FileOperation, str]] = ..., filepath: _Optional[str] = ..., filedata: _Optional[bytes] = ..., status: _Optional[_Union[FileStatus, str]] = ..., message: _Optional[str] = ..., offset: _Optional[int] = ..., length: _Optional[int] = ..., file_size: _Optional[int] = ...) -> None: ...

class I2CResult(_message.Message):
    __slots__ = ["read_data", "status"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ERROR: I2CResult.Status
    NACK_ADDRESS: I2CResult.Status
    NACK_DATA: I2CResult.Status
    OK: I2CResult.Status
    READ_DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UNSPECIFIED: I2CResult.Status
    read_data: bytes
    status: I2CResult.Status
    def __init__(self, status: _Optional[_Union[I2CResult.Status, str]] = ..., read_data: _Optional[bytes] = ...) -> None: ...

class I2CTransaction(_message.Message):
    __slots__ = ["address", "read_len", "write_data"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    READ_LEN_FIELD_NUMBER: _ClassVar[int]
    WRITE_DATA_FIELD_NUMBER: _ClassVar[int]
    address: int
    read_len: int
    write_data: bytes
    def __init__(self, address: _Optional[int] = ..., write_data: _Optional[bytes] = ..., read_len: _Optional[int] = ...) -> None: ...

class InterdeviceMessage(_message.Message):
    __slots__ = ["beep", "directory_listing", "file_transfer", "get_sd_info", "i2c_result", "i2c_scan", "i2c_scan_result", "i2c_transaction", "id", "nack", "nmea", "ping", "pong", "sd_command", "sd_info"]
    BEEP_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_LISTING_FIELD_NUMBER: _ClassVar[int]
    FILE_TRANSFER_FIELD_NUMBER: _ClassVar[int]
    GET_SD_INFO_FIELD_NUMBER: _ClassVar[int]
    I2C_RESULT_FIELD_NUMBER: _ClassVar[int]
    I2C_SCAN_FIELD_NUMBER: _ClassVar[int]
    I2C_SCAN_RESULT_FIELD_NUMBER: _ClassVar[int]
    I2C_TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NACK_FIELD_NUMBER: _ClassVar[int]
    NMEA_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    PONG_FIELD_NUMBER: _ClassVar[int]
    SD_COMMAND_FIELD_NUMBER: _ClassVar[int]
    SD_INFO_FIELD_NUMBER: _ClassVar[int]
    beep: int
    directory_listing: DirectoryListing
    file_transfer: FileTransfer
    get_sd_info: bool
    i2c_result: I2CResult
    i2c_scan: bool
    i2c_scan_result: bytes
    i2c_transaction: I2CTransaction
    id: int
    nack: bool
    nmea: str
    ping: InterdeviceVersion
    pong: InterdeviceVersion
    sd_command: SdCommand
    sd_info: SdCardInfo
    def __init__(self, id: _Optional[int] = ..., nmea: _Optional[str] = ..., beep: _Optional[int] = ..., i2c_transaction: _Optional[_Union[I2CTransaction, _Mapping]] = ..., i2c_result: _Optional[_Union[I2CResult, _Mapping]] = ..., i2c_scan: bool = ..., i2c_scan_result: _Optional[bytes] = ..., file_transfer: _Optional[_Union[FileTransfer, _Mapping]] = ..., directory_listing: _Optional[_Union[DirectoryListing, _Mapping]] = ..., get_sd_info: bool = ..., sd_info: _Optional[_Union[SdCardInfo, _Mapping]] = ..., ping: _Optional[_Union[InterdeviceVersion, str]] = ..., pong: _Optional[_Union[InterdeviceVersion, str]] = ..., nack: bool = ..., sd_command: _Optional[_Union[SdCommand, str]] = ...) -> None: ...

class SdCardInfo(_message.Message):
    __slots__ = ["busy", "card_size", "card_type", "fat_type", "free_bytes", "present", "stats_valid", "unformatted", "used_bytes"]
    class CardType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class FatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BUSY_FIELD_NUMBER: _ClassVar[int]
    CARD_SIZE_FIELD_NUMBER: _ClassVar[int]
    CARD_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXFAT: SdCardInfo.FatType
    FAT16: SdCardInfo.FatType
    FAT32: SdCardInfo.FatType
    FAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
    MMC: SdCardInfo.CardType
    NONE: SdCardInfo.CardType
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    SD: SdCardInfo.CardType
    SDHC: SdCardInfo.CardType
    SDXC: SdCardInfo.CardType
    STATS_VALID_FIELD_NUMBER: _ClassVar[int]
    UNFORMATTED_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_CARD: SdCardInfo.CardType
    UNKNOWN_FAT: SdCardInfo.FatType
    USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    busy: bool
    card_size: int
    card_type: SdCardInfo.CardType
    fat_type: SdCardInfo.FatType
    free_bytes: int
    present: bool
    stats_valid: bool
    unformatted: bool
    used_bytes: int
    def __init__(self, present: bool = ..., card_type: _Optional[_Union[SdCardInfo.CardType, str]] = ..., fat_type: _Optional[_Union[SdCardInfo.FatType, str]] = ..., card_size: _Optional[int] = ..., used_bytes: _Optional[int] = ..., free_bytes: _Optional[int] = ..., stats_valid: bool = ..., busy: bool = ..., unformatted: bool = ...) -> None: ...

class InterdeviceVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FileOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FileStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SdCommand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
