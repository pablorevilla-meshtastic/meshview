from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StoreAndForward(_message.Message):
    __slots__ = ["heartbeat", "history", "original_id", "rr", "stats", "text"]
    class RequestResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Heartbeat(_message.Message):
        __slots__ = ["period", "secondary"]
        PERIOD_FIELD_NUMBER: _ClassVar[int]
        SECONDARY_FIELD_NUMBER: _ClassVar[int]
        period: int
        secondary: int
        def __init__(self, period: _Optional[int] = ..., secondary: _Optional[int] = ...) -> None: ...
    class History(_message.Message):
        __slots__ = ["history_messages", "last_request", "window"]
        HISTORY_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        LAST_REQUEST_FIELD_NUMBER: _ClassVar[int]
        WINDOW_FIELD_NUMBER: _ClassVar[int]
        history_messages: int
        last_request: int
        window: int
        def __init__(self, history_messages: _Optional[int] = ..., window: _Optional[int] = ..., last_request: _Optional[int] = ...) -> None: ...
    class Statistics(_message.Message):
        __slots__ = ["heartbeat", "messages_max", "messages_saved", "messages_total", "requests", "requests_history", "return_max", "return_window", "up_time"]
        HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_MAX_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_SAVED_FIELD_NUMBER: _ClassVar[int]
        MESSAGES_TOTAL_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_HISTORY_FIELD_NUMBER: _ClassVar[int]
        RETURN_MAX_FIELD_NUMBER: _ClassVar[int]
        RETURN_WINDOW_FIELD_NUMBER: _ClassVar[int]
        UP_TIME_FIELD_NUMBER: _ClassVar[int]
        heartbeat: bool
        messages_max: int
        messages_saved: int
        messages_total: int
        requests: int
        requests_history: int
        return_max: int
        return_window: int
        up_time: int
        def __init__(self, messages_total: _Optional[int] = ..., messages_saved: _Optional[int] = ..., messages_max: _Optional[int] = ..., up_time: _Optional[int] = ..., requests: _Optional[int] = ..., requests_history: _Optional[int] = ..., heartbeat: bool = ..., return_max: _Optional[int] = ..., return_window: _Optional[int] = ...) -> None: ...
    CLIENT_ABORT: StoreAndForward.RequestResponse
    CLIENT_ERROR: StoreAndForward.RequestResponse
    CLIENT_HISTORY: StoreAndForward.RequestResponse
    CLIENT_PING: StoreAndForward.RequestResponse
    CLIENT_PONG: StoreAndForward.RequestResponse
    CLIENT_STATS: StoreAndForward.RequestResponse
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTER_BUSY: StoreAndForward.RequestResponse
    ROUTER_ERROR: StoreAndForward.RequestResponse
    ROUTER_HEARTBEAT: StoreAndForward.RequestResponse
    ROUTER_HISTORY: StoreAndForward.RequestResponse
    ROUTER_PING: StoreAndForward.RequestResponse
    ROUTER_PONG: StoreAndForward.RequestResponse
    ROUTER_STATS: StoreAndForward.RequestResponse
    ROUTER_TEXT_BROADCAST: StoreAndForward.RequestResponse
    ROUTER_TEXT_DIRECT: StoreAndForward.RequestResponse
    RR_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    UNSET: StoreAndForward.RequestResponse
    heartbeat: StoreAndForward.Heartbeat
    history: StoreAndForward.History
    original_id: int
    rr: StoreAndForward.RequestResponse
    stats: StoreAndForward.Statistics
    text: bytes
    def __init__(self, rr: _Optional[_Union[StoreAndForward.RequestResponse, str]] = ..., stats: _Optional[_Union[StoreAndForward.Statistics, _Mapping]] = ..., history: _Optional[_Union[StoreAndForward.History, _Mapping]] = ..., heartbeat: _Optional[_Union[StoreAndForward.Heartbeat, _Mapping]] = ..., text: _Optional[bytes] = ..., original_id: _Optional[int] = ...) -> None: ...
