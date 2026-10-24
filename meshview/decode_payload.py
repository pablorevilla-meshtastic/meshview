from google.protobuf.message import DecodeError

from meshtastic.protobuf.mesh_pb2 import (
    MeshPacket,
    NeighborInfo,
    Position,
    RouteDiscovery,
    Routing,
    User,
)
from meshtastic.protobuf.mqtt_pb2 import MapReport
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshtastic.protobuf.telemetry_pb2 import Telemetry


def text_message(payload):
    return payload.decode("utf-8")


DECODE_MAP = {
    PortNum.POSITION_APP: Position.FromString,
    PortNum.NEIGHBORINFO_APP: NeighborInfo.FromString,
    PortNum.NODEINFO_APP: User.FromString,
    PortNum.TELEMETRY_APP: Telemetry.FromString,
    PortNum.TRACEROUTE_APP: RouteDiscovery.FromString,
    PortNum.ROUTING_APP: Routing.FromString,
    PortNum.TEXT_MESSAGE_APP: text_message,
    PortNum.MAP_REPORT_APP: MapReport.FromString,
}


def enum_name(enum_type, value):
    """Return the name of a protobuf enum value, or ``unknown(N)`` if it is not defined.

    These values come from packets on the mesh, so a newer firmware or a forged packet
    can carry a number the bundled protobufs do not know. ``Name()`` raises on those.
    """
    try:
        return enum_type.Name(value)
    except ValueError:
        return f"unknown({value})"


def decode_payload(portnum, payload):
    if portnum not in DECODE_MAP:
        return None
    try:
        payload = DECODE_MAP[portnum](payload)
    except (DecodeError, UnicodeDecodeError):
        print(payload, flush=True)
        return None
    return payload


def decode(packet):
    try:
        mesh_packet = MeshPacket.FromString(packet.payload)
    except DecodeError:
        return None, None

    payload = decode_payload(mesh_packet.decoded.portnum, mesh_packet.decoded.payload)
    if payload is None:
        return mesh_packet, None

    return mesh_packet, payload
