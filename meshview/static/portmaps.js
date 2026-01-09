// Shared port label/color definitions for UI pages.
window.PORT_LABEL_MAP = {
    0: "UNKNOWN",
    1: "Text",
    3: "Position",
    4: "Node Info",
    5: "Routing",
    6: "Admin",
    8: "Waypoint",
    35: "Store Forward++",
    65: "Store & Forward",
    67: "Telemetry",
    70: "Traceroute",
    71: "Neighbor",
    73: "Map Report",
};

window.PORT_COLOR_MAP = {
    0: "#6c757d",
    1: "#007bff",
    3: "#28a745",
    4: "#ffc107",
    5: "#dc3545",
    6: "#20c997",
    8: "#fd7e14",
    35: "#8bc34a",
    65: "#6610f2",
    67: "#17a2b8",
    70: "#ff4444",
    71: "#ff66cc",
    73: "#9999ff",
};

// Aliases for pages that expect different names.
window.PORT_MAP = window.PORT_LABEL_MAP;
window.PORT_COLORS = window.PORT_COLOR_MAP;
