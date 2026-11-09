from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoRaWANBridge(_message.Message):
    __slots__ = ["chunk", "downlink", "tx_result", "uplink"]
    class Downlink(_message.Message):
        __slots__ = ["chunk_count", "freq_hz", "immediate", "invert_polarity", "may_defer", "no_crc", "payload", "payload_id", "power_dbm", "radio_params", "request_id", "tmst"]
        CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
        FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
        IMMEDIATE_FIELD_NUMBER: _ClassVar[int]
        INVERT_POLARITY_FIELD_NUMBER: _ClassVar[int]
        MAY_DEFER_FIELD_NUMBER: _ClassVar[int]
        NO_CRC_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_ID_FIELD_NUMBER: _ClassVar[int]
        POWER_DBM_FIELD_NUMBER: _ClassVar[int]
        RADIO_PARAMS_FIELD_NUMBER: _ClassVar[int]
        REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
        TMST_FIELD_NUMBER: _ClassVar[int]
        chunk_count: int
        freq_hz: int
        immediate: bool
        invert_polarity: bool
        may_defer: bool
        no_crc: bool
        payload: bytes
        payload_id: int
        power_dbm: int
        radio_params: int
        request_id: int
        tmst: int
        def __init__(self, freq_hz: _Optional[int] = ..., tmst: _Optional[int] = ..., radio_params: _Optional[int] = ..., power_dbm: _Optional[int] = ..., immediate: bool = ..., invert_polarity: bool = ..., no_crc: bool = ..., may_defer: bool = ..., request_id: _Optional[int] = ..., payload: _Optional[bytes] = ..., payload_id: _Optional[int] = ..., chunk_count: _Optional[int] = ...) -> None: ...
    class PayloadChunk(_message.Message):
        __slots__ = ["chunk_index", "payload_chunk", "payload_id"]
        CHUNK_INDEX_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_CHUNK_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_ID_FIELD_NUMBER: _ClassVar[int]
        chunk_index: int
        payload_chunk: bytes
        payload_id: int
        def __init__(self, payload_id: _Optional[int] = ..., chunk_index: _Optional[int] = ..., payload_chunk: _Optional[bytes] = ...) -> None: ...
    class TxResult(_message.Message):
        __slots__ = ["request_id", "status", "tmst"]
        class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        COLLISION_BEACON: LoRaWANBridge.TxResult.Status
        COLLISION_PACKET: LoRaWANBridge.TxResult.Status
        DEFERRED: LoRaWANBridge.TxResult.Status
        DROPPED: LoRaWANBridge.TxResult.Status
        GPS_UNLOCKED: LoRaWANBridge.TxResult.Status
        NONE: LoRaWANBridge.TxResult.Status
        REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TMST_FIELD_NUMBER: _ClassVar[int]
        TOO_EARLY: LoRaWANBridge.TxResult.Status
        TOO_LATE: LoRaWANBridge.TxResult.Status
        TX_FREQ: LoRaWANBridge.TxResult.Status
        TX_POWER: LoRaWANBridge.TxResult.Status
        request_id: int
        status: LoRaWANBridge.TxResult.Status
        tmst: int
        def __init__(self, tmst: _Optional[int] = ..., status: _Optional[_Union[LoRaWANBridge.TxResult.Status, str]] = ..., request_id: _Optional[int] = ...) -> None: ...
    class Uplink(_message.Message):
        __slots__ = ["chunk_count", "freq_hz", "fsk_bitrate", "payload", "payload_id", "radio_params", "rssi_x10", "snr_x10", "tmst"]
        CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
        FREQ_HZ_FIELD_NUMBER: _ClassVar[int]
        FSK_BITRATE_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_ID_FIELD_NUMBER: _ClassVar[int]
        RADIO_PARAMS_FIELD_NUMBER: _ClassVar[int]
        RSSI_X10_FIELD_NUMBER: _ClassVar[int]
        SNR_X10_FIELD_NUMBER: _ClassVar[int]
        TMST_FIELD_NUMBER: _ClassVar[int]
        chunk_count: int
        freq_hz: int
        fsk_bitrate: int
        payload: bytes
        payload_id: int
        radio_params: int
        rssi_x10: int
        snr_x10: int
        tmst: int
        def __init__(self, freq_hz: _Optional[int] = ..., tmst: _Optional[int] = ..., rssi_x10: _Optional[int] = ..., snr_x10: _Optional[int] = ..., radio_params: _Optional[int] = ..., fsk_bitrate: _Optional[int] = ..., payload: _Optional[bytes] = ..., payload_id: _Optional[int] = ..., chunk_count: _Optional[int] = ...) -> None: ...
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    DOWNLINK_FIELD_NUMBER: _ClassVar[int]
    TX_RESULT_FIELD_NUMBER: _ClassVar[int]
    UPLINK_FIELD_NUMBER: _ClassVar[int]
    chunk: LoRaWANBridge.PayloadChunk
    downlink: LoRaWANBridge.Downlink
    tx_result: LoRaWANBridge.TxResult
    uplink: LoRaWANBridge.Uplink
    def __init__(self, uplink: _Optional[_Union[LoRaWANBridge.Uplink, _Mapping]] = ..., downlink: _Optional[_Union[LoRaWANBridge.Downlink, _Mapping]] = ..., tx_result: _Optional[_Union[LoRaWANBridge.TxResult, _Mapping]] = ..., chunk: _Optional[_Union[LoRaWANBridge.PayloadChunk, _Mapping]] = ...) -> None: ...
