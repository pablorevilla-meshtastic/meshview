// Shared port label/color definitions for UI pages.
// Port numbers defined in: https://github.com/meshtastic/protobufs/blob/master/meshtastic/portnums.proto
window.PORT_LABEL_MAP = {
    0: MeshI18n.t("Unknown"),
    1: MeshI18n.t("Text"),
    2: MeshI18n.t("Remote Hardware"),
    3: MeshI18n.t("Position"),
    4: MeshI18n.t("Node Info"),
    5: MeshI18n.t("Routing"),
    6: MeshI18n.t("Admin"),
    7: MeshI18n.t("Text (Compressed)"),
    8: MeshI18n.t("Waypoint"),
    9: MeshI18n.t("Audio"),
    10: MeshI18n.t("Detection Sensor"),
    11: MeshI18n.t("Alert"),
    12: MeshI18n.t("Key Verification"),
    32: MeshI18n.t("Reply"),
    33: MeshI18n.t("IP Tunnel"),
    34: "Paxcounter",
    35: "Store Forward++",
    36: MeshI18n.t("Node Status"),
    64: MeshI18n.t("Serial"),
    65: MeshI18n.t("Store & Forward"),
    66: MeshI18n.t("Range Test"),
    67: MeshI18n.t("Telemetry"),
    68: "ZPS",
    69: MeshI18n.t("Simulator"),
    70: MeshI18n.t("Traceroute"),
    71: MeshI18n.t("Neighbor"),
    72: "ATAK",
    73: MeshI18n.t("Map Report"),
    74: MeshI18n.t("Power Stress"),
    76: MeshI18n.t("Reticulum Tunnel"),
    77: "Cayenne",
    256: MeshI18n.t("Private App"),
    257: MeshI18n.t("ATAK Forwarder"),
};

window.PORT_COLOR_MAP = {
    0: "#6c757d",   // gray - Unknown
    1: "#1f77b4",   // blue - Text
    2: "#795548",   // brown - Remote Hardware
    3: "#2ca02c",   // green - Position
    4: "#ffbf00",   // yellow - Node Info
    5: "#ff7f0e",   // orange - Routing
    6: "#20c997",   // teal - Admin
    7: "#6a51a3",   // purple - Text (Compressed)
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
    70: "#f44336",  // bright red - Traceroute
    71: "#e377c2",  // pink - Neighbor
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
