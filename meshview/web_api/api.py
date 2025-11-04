"""API endpoints for MeshView."""
import datetime
import json
import logging
import os
import re

from aiohttp import web
from sqlalchemy import text

from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import database, decode_payload, store
from meshview.__version__ import __version__, _git_revision_short, get_version_info
from meshview.config import CONFIG

logger = logging.getLogger(__name__)

# Will be set by web.py during initialization
Packet = None
SEQ_REGEX = None
LANG_DIR = None

# Create dedicated route table for API endpoints
routes = web.RouteTableDef()


def init_api_module(packet_class, seq_regex, lang_dir):
    """Initialize API module with dependencies from main web module."""
    global Packet, SEQ_REGEX, LANG_DIR
    Packet = packet_class
    SEQ_REGEX = seq_regex
    LANG_DIR = lang_dir


@routes.get("/api/channels")
async def api_channels(request: web.Request):
    period_type = request.query.get("period_type", "hour")
    length = int(request.query.get("length", 24))

    try:
        channels = await store.get_channels_in_period(period_type, length)
        return web.json_response({"channels": channels})
    except Exception as e:
        return web.json_response({"channels": [], "error": str(e)})

@routes.get("/api/chat")
async def api_chat(request):
    try:
        # Parse query params
        limit_str = request.query.get("limit", "20")
        since_str = request.query.get("since")

        # Clamp limit between 1 and 200
        try:
            limit = min(max(int(limit_str), 1), 100)
        except ValueError:
            limit = 50

        # Parse "since" timestamp if provided
        since = None
        if since_str:
            try:
                since = datetime.datetime.fromisoformat(since_str)
            except Exception as e:
                logger.error(f"Failed to parse since '{since_str}': {e}")

        # Fetch packets from store
        packets = await store.get_packets(
            node_id=0xFFFFFFFF,
            portnum=PortNum.TEXT_MESSAGE_APP,
            limit=limit,
        )

        ui_packets = [Packet.from_model(p) for p in packets]

        # Filter out "seq N" and missing payloads
        filtered_packets = [
            p for p in ui_packets if p.payload and not SEQ_REGEX.fullmatch(p.payload)
        ]

        # Apply "since" filter
        if since:
            filtered_packets = [p for p in filtered_packets if p.import_time > since]

        # Sort by import_time descending (latest first)
        filtered_packets.sort(key=lambda p: p.import_time, reverse=True)

        # Trim to requested limit
        filtered_packets = filtered_packets[:limit]

        # Build response data
        packets_data = []
        for p in filtered_packets:
            reply_id = getattr(
                getattr(getattr(p, "raw_mesh_packet", None), "decoded", None), "reply_id", None
            )

            packet_dict = {
                "id": p.id,
                "import_time": p.import_time.isoformat(),
                "channel": getattr(p.from_node, "channel", ""),
                "from_node_id": p.from_node_id,
                "long_name": getattr(p.from_node, "long_name", ""),
                "payload": p.payload,
            }

            if reply_id:
                packet_dict["reply_id"] = reply_id

            packets_data.append(packet_dict)

        # Pick latest import time for clients to use in next request
        if filtered_packets:
            latest_import_time = filtered_packets[0].import_time.isoformat()
        elif since:
            latest_import_time = since.isoformat()
        else:
            latest_import_time = None

        return web.json_response(
            {
                "packets": packets_data,
                "latest_import_time": latest_import_time,
            }
        )

    except Exception as e:
        logger.error(f"Error in /api/chat: {e}")
        return web.json_response(
            {"error": "Failed to fetch chat data", "details": str(e)}, status=500
        )

@routes.get("/api/nodes")
async def api_nodes(request):
    try:
        # Optional query parameters
        role = request.query.get("role")
        channel = request.query.get("channel")
        hw_model = request.query.get("hw_model")
        days_active = request.query.get("days_active")

        if days_active:
            try:
                days_active = int(days_active)
            except ValueError:
                days_active = None

        # Fetch nodes from database
        nodes = await store.get_nodes(
            role=role, channel=channel, hw_model=hw_model, days_active=days_active
        )

        # Prepare the JSON response
        nodes_data = []
        for n in nodes:
            nodes_data.append(
                {
                    "id": getattr(n, "id", None),
                    "node_id": n.node_id,
                    "long_name": n.long_name,
                    "short_name": n.short_name,
                    "hw_model": n.hw_model,
                    "firmware": n.firmware,
                    "role": n.role,
                    "last_lat": getattr(n, "last_lat", None),
                    "last_long": getattr(n, "last_long", None),
                    "channel": n.channel,
                    "last_update": n.last_update.isoformat(),
                }
            )

        return web.json_response({"nodes": nodes_data})

    except Exception as e:
        logger.error(f"Error in /api/nodes: {e}")
        return web.json_response({"error": "Failed to fetch nodes"}, status=500)

@routes.get("/api/packets")
async def api_packets(request):
    try:
        # Query parameters
        limit = int(request.query.get("limit", 50))
        since_str = request.query.get("since")
        since_time = None

        if since_str:
            try:
                # Robust ISO 8601 parsing (handles 'Z' for UTC)
                since_time = datetime.datetime.fromisoformat(since_str.replace("Z", "+00:00"))
            except Exception as e:
                logger.error(f"Failed to parse 'since' timestamp '{since_str}': {e}")

        # Fetch packets from the store
        packets = await store.get_packets(limit=limit, after=since_time)
        packets = [Packet.from_model(p) for p in packets]

        packets_json = []
        for p in packets:
            payload = (p.payload or "").strip()

            packets_json.append(
                {
                    "id": p.id,
                    "from_node_id": p.from_node_id,
                    "to_node_id": p.to_node_id,
                    "portnum": int(p.portnum) if p.portnum is not None else None,
                    "import_time": p.import_time.isoformat(),
                    "payload": payload,
                }
            )

        return web.json_response({"packets": packets_json})

    except Exception as e:
        logger.error(f"Error in /api/packets: {e}")
        return web.json_response({"error": "Failed to fetch packets"}, status=500)

@routes.get("/api/stats")
async def api_stats(request):
    """
    Return packet statistics for a given period type, length,
    and optional filters for channel, portnum, to_node, from_node.
    """
    allowed_periods = {"hour", "day"}

    # period_type validation
    period_type = request.query.get("period_type", "hour").lower()
    if period_type not in allowed_periods:
        return web.json_response(
            {"error": f"Invalid period_type. Must be one of {allowed_periods}"}, status=400
        )

    # length validation
    try:
        length = int(request.query.get("length", 24))
    except ValueError:
        return web.json_response({"error": "length must be an integer"}, status=400)

    # Optional filters
    channel = request.query.get("channel")

    def parse_int_param(name):
        value = request.query.get(name)
        if value is not None:
            try:
                return int(value)
            except ValueError:
                raise web.HTTPBadRequest(
                    text=json.dumps({"error": f"{name} must be an integer"}),
                    content_type="application/json",
                ) from None
        return None

    portnum = parse_int_param("portnum")
    to_node = parse_int_param("to_node")
    from_node = parse_int_param("from_node")

    # Fetch stats
    stats = await store.get_packet_stats(
        period_type=period_type,
        length=length,
        channel=channel,
        portnum=portnum,
        to_node=to_node,
        from_node=from_node,
    )

    return web.json_response(stats)

@routes.get("/api/edges")
async def api_edges(request):
    since = datetime.datetime.now() - datetime.timedelta(hours=48)
    filter_type = request.query.get("type")

    edges = {}

    # Only build traceroute edges if requested
    if filter_type in (None, "traceroute"):
        async for tr in store.get_traceroutes(since):
            try:
                route = decode_payload.decode_payload(PortNum.TRACEROUTE_APP, tr.route)
            except Exception as e:
                logger.error(f"Error decoding Traceroute {tr.id}: {e}")
                continue

            path = [tr.packet.from_node_id] + list(route.route)
            path.append(tr.packet.to_node_id if tr.done else tr.gateway_node_id)

            for a, b in zip(path, path[1:], strict=False):
                edges[(a, b)] = "traceroute"

    # Only build neighbor edges if requested
    if filter_type in (None, "neighbor"):
        packets = await store.get_packets(portnum=PortNum.NEIGHBORINFO_APP, after=since)
        for packet in packets:
            try:
                _, neighbor_info = decode_payload.decode(packet)
                for node in neighbor_info.neighbors:
                    edges.setdefault((node.node_id, packet.from_node_id), "neighbor")
            except Exception as e:
                logger.error(
                    f"Error decoding NeighborInfo packet {getattr(packet, 'id', '?')}: {e}"
                )

    # Convert edges dict to list format for JSON response
    edges_list = [
        {"from": frm, "to": to, "type": edge_type} for (frm, to), edge_type in edges.items()
    ]

    return web.json_response({"edges": edges_list})

@routes.get("/api/config")
async def api_config(request):
    try:
        # ------------------ Helpers ------------------
        def get(section, key, default=None):
            """Safe getter for both dict and ConfigParser."""
            if isinstance(section, dict):
                return section.get(key, default)
            return section.get(key, fallback=default)

        def get_bool(section, key, default=False):
            val = get(section, key, default)
            if isinstance(val, bool):
                return "true" if val else "false"
            if isinstance(val, str):
                return "true" if val.lower() in ("1", "true", "yes", "on") else "false"
            return "true" if bool(val) else "false"

        def get_float(section, key, default=0.0):
            try:
                return float(get(section, key, default))
            except Exception:
                return float(default)

        def get_int(section, key, default=0):
            try:
                return int(get(section, key, default))
            except Exception:
                return default

        def get_str(section, key, default=""):
            val = get(section, key, default)
            return str(val) if val is not None else str(default)

        # ------------------ SITE ------------------
        site = CONFIG.get("site", {})
        safe_site = {
            "domain": get_str(site, "domain", ""),
            "language": get_str(site, "language", "en"),
            "title": get_str(site, "title", ""),
            "message": get_str(site, "message", ""),
            "starting": get_str(site, "starting", "/chat"),
            "nodes": get_bool(site, "nodes", True),
            "conversations": get_bool(site, "conversations", True),
            "everything": get_bool(site, "everything", True),
            "graphs": get_bool(site, "graphs", True),
            "stats": get_bool(site, "stats", True),
            "net": get_bool(site, "net", True),
            "map": get_bool(site, "map", True),
            "top": get_bool(site, "top", True),
            "map_top_left_lat": get_float(site, "map_top_left_lat", 39.0),
            "map_top_left_lon": get_float(site, "map_top_left_lon", -123.0),
            "map_bottom_right_lat": get_float(site, "map_bottom_right_lat", 36.0),
            "map_bottom_right_lon": get_float(site, "map_bottom_right_lon", -121.0),
            "map_interval": get_int(site, "map_interval", 3),
            "firehose_interval": get_int(site, "firehose_interval", 3),
            "weekly_net_message": get_str(
                site, "weekly_net_message", "Weekly Mesh check-in message."
            ),
            "net_tag": get_str(site, "net_tag", "#BayMeshNet"),
            "version": str(__version__),
        }

        # ------------------ MQTT ------------------
        mqtt = CONFIG.get("mqtt", {})
        topics_raw = get(mqtt, "topics", [])

        if isinstance(topics_raw, str):
            try:
                topics = json.loads(topics_raw)
            except Exception:
                topics = [topics_raw]
        elif isinstance(topics_raw, list):
            topics = topics_raw
        else:
            topics = []

        safe_mqtt = {
            "server": get_str(mqtt, "server", ""),
            "topics": topics,
        }

        # ------------------ CLEANUP ------------------
        cleanup = CONFIG.get("cleanup", {})
        safe_cleanup = {
            "enabled": get_bool(cleanup, "enabled", False),
            "days_to_keep": get_str(cleanup, "days_to_keep", "14"),
            "hour": get_str(cleanup, "hour", "2"),
            "minute": get_str(cleanup, "minute", "0"),
            "vacuum": get_bool(cleanup, "vacuum", False),
        }

        safe_config = {
            "site": safe_site,
            "mqtt": safe_mqtt,
            "cleanup": safe_cleanup,
        }

        return web.json_response(safe_config)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

@routes.get("/api/lang")
async def api_lang(request):
    # Language from ?lang=xx, fallback to config, then to "en"
    lang_code = request.query.get("lang") or CONFIG.get("site", {}).get("language", "en")
    section = request.query.get("section")

    lang_file = os.path.join(LANG_DIR, f"{lang_code}.json")
    if not os.path.exists(lang_file):
        lang_file = os.path.join(LANG_DIR, "en.json")

    # Load JSON translations
    with open(lang_file, encoding="utf-8") as f:
        translations = json.load(f)

    if section:
        section = section.lower()
        if section in translations:
            return web.json_response(translations[section])
        else:
            return web.json_response(
                {"error": f"Section '{section}' not found in {lang_code}"}, status=404
            )

    # if no section requested → return full translation file
    return web.json_response(translations)

@routes.get("/health")
async def health_check(request):
    """Health check endpoint for monitoring and load balancers."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "version": __version__,
        "git_revision": _git_revision_short,
    }

    # Check database connectivity
    try:
        async with database.async_session() as session:
            await session.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        return web.json_response(health_status, status=503)

    return web.json_response(health_status)

@routes.get("/version")
async def version_endpoint(request):
    """Return version information including semver and git revision."""
    try:
        version_info = get_version_info()
        return web.json_response(version_info)
    except Exception as e:
        logger.error(f"Error in /version: {e}")
        return web.json_response({"error": "Failed to fetch version info"}, status=500)
