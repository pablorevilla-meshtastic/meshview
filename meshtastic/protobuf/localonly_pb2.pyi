from meshtastic.protobuf import config_pb2 as _config_pb2
from meshtastic.protobuf import module_config_pb2 as _module_config_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocalConfig(_message.Message):
    __slots__ = ["bluetooth", "device", "display", "lora", "network", "position", "power", "security", "version"]
    BLUETOOTH_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    LORA_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    bluetooth: _config_pb2.Config.BluetoothConfig
    device: _config_pb2.Config.DeviceConfig
    display: _config_pb2.Config.DisplayConfig
    lora: _config_pb2.Config.LoRaConfig
    network: _config_pb2.Config.NetworkConfig
    position: _config_pb2.Config.PositionConfig
    power: _config_pb2.Config.PowerConfig
    security: _config_pb2.Config.SecurityConfig
    version: int
    def __init__(self, device: _Optional[_Union[_config_pb2.Config.DeviceConfig, _Mapping]] = ..., position: _Optional[_Union[_config_pb2.Config.PositionConfig, _Mapping]] = ..., power: _Optional[_Union[_config_pb2.Config.PowerConfig, _Mapping]] = ..., network: _Optional[_Union[_config_pb2.Config.NetworkConfig, _Mapping]] = ..., display: _Optional[_Union[_config_pb2.Config.DisplayConfig, _Mapping]] = ..., lora: _Optional[_Union[_config_pb2.Config.LoRaConfig, _Mapping]] = ..., bluetooth: _Optional[_Union[_config_pb2.Config.BluetoothConfig, _Mapping]] = ..., version: _Optional[int] = ..., security: _Optional[_Union[_config_pb2.Config.SecurityConfig, _Mapping]] = ...) -> None: ...

class LocalModuleConfig(_message.Message):
    __slots__ = ["ambient_lighting", "audio", "canned_message", "detection_sensor", "external_notification", "mesh_beacon", "mqtt", "neighbor_info", "paxcounter", "range_test", "remote_hardware", "serial", "statusmessage", "store_forward", "tak", "telemetry", "traffic_management", "version"]
    AMBIENT_LIGHTING_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    CANNED_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETECTION_SENSOR_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    MESH_BEACON_FIELD_NUMBER: _ClassVar[int]
    MQTT_FIELD_NUMBER: _ClassVar[int]
    NEIGHBOR_INFO_FIELD_NUMBER: _ClassVar[int]
    PAXCOUNTER_FIELD_NUMBER: _ClassVar[int]
    RANGE_TEST_FIELD_NUMBER: _ClassVar[int]
    REMOTE_HARDWARE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_FIELD_NUMBER: _ClassVar[int]
    STATUSMESSAGE_FIELD_NUMBER: _ClassVar[int]
    STORE_FORWARD_FIELD_NUMBER: _ClassVar[int]
    TAK_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ambient_lighting: _module_config_pb2.ModuleConfig.AmbientLightingConfig
    audio: _module_config_pb2.ModuleConfig.AudioConfig
    canned_message: _module_config_pb2.ModuleConfig.CannedMessageConfig
    detection_sensor: _module_config_pb2.ModuleConfig.DetectionSensorConfig
    external_notification: _module_config_pb2.ModuleConfig.ExternalNotificationConfig
    mesh_beacon: _module_config_pb2.ModuleConfig.MeshBeaconConfig
    mqtt: _module_config_pb2.ModuleConfig.MQTTConfig
    neighbor_info: _module_config_pb2.ModuleConfig.NeighborInfoConfig
    paxcounter: _module_config_pb2.ModuleConfig.PaxcounterConfig
    range_test: _module_config_pb2.ModuleConfig.RangeTestConfig
    remote_hardware: _module_config_pb2.ModuleConfig.RemoteHardwareConfig
    serial: _module_config_pb2.ModuleConfig.SerialConfig
    statusmessage: _module_config_pb2.ModuleConfig.StatusMessageConfig
    store_forward: _module_config_pb2.ModuleConfig.StoreForwardConfig
    tak: _module_config_pb2.ModuleConfig.TAKConfig
    telemetry: _module_config_pb2.ModuleConfig.TelemetryConfig
    traffic_management: _module_config_pb2.ModuleConfig.TrafficManagementConfig
    version: int
    def __init__(self, mqtt: _Optional[_Union[_module_config_pb2.ModuleConfig.MQTTConfig, _Mapping]] = ..., serial: _Optional[_Union[_module_config_pb2.ModuleConfig.SerialConfig, _Mapping]] = ..., external_notification: _Optional[_Union[_module_config_pb2.ModuleConfig.ExternalNotificationConfig, _Mapping]] = ..., store_forward: _Optional[_Union[_module_config_pb2.ModuleConfig.StoreForwardConfig, _Mapping]] = ..., range_test: _Optional[_Union[_module_config_pb2.ModuleConfig.RangeTestConfig, _Mapping]] = ..., telemetry: _Optional[_Union[_module_config_pb2.ModuleConfig.TelemetryConfig, _Mapping]] = ..., canned_message: _Optional[_Union[_module_config_pb2.ModuleConfig.CannedMessageConfig, _Mapping]] = ..., audio: _Optional[_Union[_module_config_pb2.ModuleConfig.AudioConfig, _Mapping]] = ..., remote_hardware: _Optional[_Union[_module_config_pb2.ModuleConfig.RemoteHardwareConfig, _Mapping]] = ..., neighbor_info: _Optional[_Union[_module_config_pb2.ModuleConfig.NeighborInfoConfig, _Mapping]] = ..., ambient_lighting: _Optional[_Union[_module_config_pb2.ModuleConfig.AmbientLightingConfig, _Mapping]] = ..., detection_sensor: _Optional[_Union[_module_config_pb2.ModuleConfig.DetectionSensorConfig, _Mapping]] = ..., paxcounter: _Optional[_Union[_module_config_pb2.ModuleConfig.PaxcounterConfig, _Mapping]] = ..., statusmessage: _Optional[_Union[_module_config_pb2.ModuleConfig.StatusMessageConfig, _Mapping]] = ..., traffic_management: _Optional[_Union[_module_config_pb2.ModuleConfig.TrafficManagementConfig, _Mapping]] = ..., tak: _Optional[_Union[_module_config_pb2.ModuleConfig.TAKConfig, _Mapping]] = ..., mesh_beacon: _Optional[_Union[_module_config_pb2.ModuleConfig.MeshBeaconConfig, _Mapping]] = ..., version: _Optional[int] = ...) -> None: ...
