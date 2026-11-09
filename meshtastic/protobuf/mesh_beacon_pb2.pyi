from meshtastic.protobuf import channel_pb2 as _channel_pb2
from meshtastic.protobuf import config_pb2 as _config_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeshBeacon(_message.Message):
    __slots__ = ["message", "offer_channel", "offer_frequency_slot", "offer_preset", "offer_region"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OFFER_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    OFFER_FREQUENCY_SLOT_FIELD_NUMBER: _ClassVar[int]
    OFFER_PRESET_FIELD_NUMBER: _ClassVar[int]
    OFFER_REGION_FIELD_NUMBER: _ClassVar[int]
    message: str
    offer_channel: _channel_pb2.ChannelSettings
    offer_frequency_slot: int
    offer_preset: _config_pb2.Config.LoRaConfig.ModemPreset
    offer_region: _config_pb2.Config.LoRaConfig.RegionCode
    def __init__(self, message: _Optional[str] = ..., offer_channel: _Optional[_Union[_channel_pb2.ChannelSettings, _Mapping]] = ..., offer_region: _Optional[_Union[_config_pb2.Config.LoRaConfig.RegionCode, str]] = ..., offer_preset: _Optional[_Union[_config_pb2.Config.LoRaConfig.ModemPreset, str]] = ..., offer_frequency_slot: _Optional[int] = ...) -> None: ...
