// Shared port label/color definitions for UI pages.
// Port numbers defined in: https://github.com/meshtastic/protobufs/blob/master/meshtastic/portnums.proto
window.PORT_LABEL_MAP = {
    0: "Unknown",
    1: "Text",
    2: "Remote Hardware",
    3: "Position",
    4: "Node Info",
    5: "Routing",
    6: "Admin",
    7: "Text (Compressed)",
    8: "Waypoint",
    9: "Audio",
    10: "Detection Sensor",
    11: "Alert",
    12: "Key Verification",
    32: "Reply",
    33: "IP Tunnel",
    34: "Paxcounter",
    35: "Store Forward++",
    36: "Node Status",
    64: "Serial",
    65: "Store & Forward",
    66: "Range Test",
    67: "Telemetry",
    68: "ZPS",
    69: "Simulator",
    70: "Traceroute",
    71: "Neighbor",
    72: "ATAK",
    73: "Map Report",
    74: "Power Stress",
    76: "Reticulum Tunnel",
    77: "Cayenne",
    256: "Private App",
    257: "ATAK Forwarder",
};

window.PORT_COLOR_MAP = {
    0: "#6c757d",   // gray - Unknown
    1: "#007bff",   // blue - Text
    2: "#795548",   // brown - Remote Hardware
    3: "#28a745",   // green - Position
    4: "#ffc107",   // yellow - Node Info
    5: "#dc3545",   // red - Routing
    6: "#20c997",   // teal - Admin
    7: "#0056b3",   // dark blue - Text (Compressed)
    8: "#fd7e14",   // orange - Waypoint
    9: "#e91e63",   // pink - Audio
    10: "#ff9800",  // amber - Detection Sensor
    11: "#f44336",  // bright red - Alert
    12: "#9c27b0",  // purple - Key Verification
    32: "#00bcd4",  // cyan - Reply
    33: "#607d8b",  // blue-gray - IP Tunnel
    34: "#8d6e63",  // brown-gray - Paxcounter
    35: "#8bc34a",  // light green - Store Forward++
    36: "#4caf50",  // green - Node Status
    64: "#9e9e9e",  // gray - Serial
    65: "#6610f2",  // indigo - Store & Forward
    66: "#cddc39",  // lime - Range Test
    67: "#17a2b8",  // info blue - Telemetry
    68: "#3f51b5",  // indigo - ZPS
    69: "#673ab7",  // deep purple - Simulator
    70: "#ff4444",  // red - Traceroute
    71: "#ff66cc",  // pink - Neighbor
    72: "#2196f3",  // blue - ATAK
    73: "#9999ff",  // light purple - Map Report
    74: "#ff5722",  // deep orange - Power Stress
    76: "#009688",  // teal - Reticulum Tunnel
    77: "#4db6ac",  // teal accent - Cayenne
    256: "#757575", // dark gray - Private App
    257: "#1976d2", // blue - ATAK Forwarder
};

// Aliases for pages that expect different names.
window.PORT_MAP = window.PORT_LABEL_MAP;
window.PORT_COLORS = window.PORT_COLOR_MAP;
