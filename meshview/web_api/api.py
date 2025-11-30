"""API endpoints for MeshView."""

import datetime
import json
import logging
import os

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
                    # "last_update": n.last_update.isoformat(),
                    "last_seen_us": n.last_seen_us,
                }
            )

        return web.json_response({"nodes": nodes_data})

    except Exception as e:
        logger.error(f"Error in /api/nodes: {e}")
        return web.json_response({"error": "Failed to fetch nodes"}, status=500)


@routes.get("/api/packets")
async def api_packets(request):
    try:
        # --- Parse query parameters ---
        packet_id_str = request.query.get("packet_id")
        limit_str = request.query.get("limit", "50")
        since_str = request.query.get("since")
        portnum_str = request.query.get("portnum")
        contains = request.query.get("contains")

        # NEW — explicit filters
        from_node_id_str = request.query.get("from_node_id")
        to_node_id_str = request.query.get("to_node_id")
        node_id_str = request.query.get("node_id")  # legacy: match either from/to

        # --- If a packet_id is provided, return only that packet ---
        if packet_id_str:
            try:
                packet_id = int(packet_id_str)
            except ValueError:
                return web.json_response({"error": "Invalid packet_id format"}, status=400)

            packet = await store.get_packet(packet_id)
            if not packet:
                return web.json_response({"packets": []})

            p = Packet.from_model(packet)
            data = {
                "id": p.id,
                "from_node_id": p.from_node_id,
                "to_node_id": p.to_node_id,
                "portnum": int(p.portnum) if p.portnum is not None else None,
                "payload": (p.payload or "").strip(),
                "import_time_us": p.import_time_us,
                "import_time": p.import_time.isoformat() if p.import_time else None,
                "channel": getattr(p.from_node, "channel", ""),
                "long_name": getattr(p.from_node, "long_name", ""),
            }
            return web.json_response({"packets": [data]})

        # --- Parse limit ---
        try:
            limit = min(max(int(limit_str), 1), 100)
        except ValueError:
            limit = 50

        # --- Parse since timestamp ---
        since = None
        if since_str:
            try:
                since = int(since_str)
            except ValueError:
                logger.warning(f"Invalid 'since' value (expected microseconds): {since_str}")

        # --- Parse portnum ---
        portnum = None
        if portnum_str:
            try:
                portnum = int(portnum_str)
            except ValueError:
                logger.warning(f"Invalid portnum: {portnum_str}")

        # --- Parse node filters ---
        from_node_id = None
        to_node_id = None
        node_id = None  # legacy: match either from/to

        if from_node_id_str:
            try:
                from_node_id = int(from_node_id_str, 0)
            except ValueError:
                logger.warning(f"Invalid from_node_id: {from_node_id_str}")

        if to_node_id_str:
            try:
                to_node_id = int(to_node_id_str, 0)
            except ValueError:
                logger.warning(f"Invalid to_node_id: {to_node_id_str}")

        if node_id_str:
            try:
                node_id = int(node_id_str, 0)
            except ValueError:
                logger.warning(f"Invalid node_id: {node_id_str}")

        # --- Fetch packets using explicit filters ---
        packets = await store.get_packets(
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            node_id=node_id,
            portnum=portnum,
            after=since,
            contains=contains,
            limit=limit,
        )

        ui_packets = [Packet.from_model(p) for p in packets]

        # --- Text message filtering ---
        if portnum == PortNum.TEXT_MESSAGE_APP:
            ui_packets = [p for p in ui_packets if p.payload and not SEQ_REGEX.fullmatch(p.payload)]
            if contains:
                ui_packets = [p for p in ui_packets if contains.lower() in p.payload.lower()]

        # --- Sort descending by import_time_us ---
        ui_packets.sort(
            key=lambda p: (p.import_time_us is not None, p.import_time_us or 0), reverse=True
        )
        ui_packets = ui_packets[:limit]

        # --- Build JSON output ---
        packets_data = []
        for p in ui_packets:
            packet_dict = {
                "id": p.id,
                "import_time_us": p.import_time_us,
                "import_time": p.import_time.isoformat() if p.import_time else None,
                "channel": getattr(p.from_node, "channel", ""),
                "from_node_id": p.from_node_id,
                "to_node_id": p.to_node_id,
                "portnum": int(p.portnum),
                "long_name": getattr(p.from_node, "long_name", ""),
                "payload": (p.payload or "").strip(),
            }

            reply_id = getattr(
                getattr(getattr(p, "raw_mesh_packet", None), "decoded", None),
                "reply_id",
                None,
            )
            if reply_id:
                packet_dict["reply_id"] = reply_id

            packets_data.append(packet_dict)

        # --- Latest import_time for incremental fetch ---
        latest_import_time = None
        if packets_data:
            for p in packets_data:
                if p.get("import_time_us") and p["import_time_us"] > 0:
                    latest_import_time = max(latest_import_time or 0, p["import_time_us"])
                elif p.get("import_time") and latest_import_time is None:
                    try:
                        dt = datetime.datetime.fromisoformat(
                            p["import_time"].replace("Z", "+00:00")
                        )
                        latest_import_time = int(dt.timestamp() * 1_000_000)
                    except Exception:
                        pass

        response = {"packets": packets_data}
        if latest_import_time is not None:
            response["latest_import_time"] = latest_import_time

        return web.json_response(response)

    except Exception as e:
        logger.error(f"Error in /api/packets: {e}")
        return web.json_response({"error": "Failed to fetch packets"}, status=500)


@routes.get("/api/stats")
async def api_stats(request):
    """
    Enhanced stats endpoint:
    - Supports global stats (existing behavior)
    - Supports per-node stats using ?node=<node_id>
      returning both sent AND seen counts in the specified period
    """
    allowed_periods = {"hour", "day"}

    period_type = request.query.get("period_type", "hour").lower()
    if period_type not in allowed_periods:
        return web.json_response(
            {"error": f"Invalid period_type. Must be one of {allowed_periods}"},
            status=400,
        )

    try:
        length = int(request.query.get("length", 24))
    except ValueError:
        return web.json_response({"error": "length must be an integer"}, status=400)

    # NEW: optional combined node stats
    node_str = request.query.get("node")
    if node_str:
        try:
            node_id = int(node_str)
        except ValueError:
            return web.json_response({"error": "node must be an integer"}, status=400)

        # Fetch sent packets
        sent = await store.get_packet_stats(
            period_type=period_type,
            length=length,
            from_node=node_id,
        )

        # Fetch seen packets
        seen = await store.get_packet_stats(
            period_type=period_type,
            length=length,
            to_node=node_id,
        )

        return web.json_response(
            {
                "node_id": node_id,
                "period_type": period_type,
                "length": length,
                "sent": sent.get("total", 0),
                "seen": seen.get("total", 0),
            }
        )

    # ---- Existing full stats mode (unchanged) ----
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

    stats = await store.get_packet_stats(
        period_type=period_type,
        length=length,
        channel=channel,
        portnum=portnum,
        to_node=to_node,
        from_node=from_node,
    )

    return web.json_response(stats)


@routes.get("/api/stats/count")
async def api_stats_count(request):
    """
    Returns packet and packet_seen totals.
    Behavior:
      • If no filters → total packets ever + total seen ever
      • If filters → apply window/channel/from/to + packet_id
    """

    # -------- Parse request parameters --------
    packet_id_str = request.query.get("packet_id")
    packet_id = None
    if packet_id_str:
        try:
            packet_id = int(packet_id_str)
        except ValueError:
            return web.json_response({"error": "packet_id must be integer"}, status=400)

    period_type = request.query.get("period_type")
    length_str = request.query.get("length")
    length = None
    if length_str:
        try:
            length = int(length_str)
        except ValueError:
            return web.json_response({"error": "length must be integer"}, status=400)

    channel = request.query.get("channel")

    def parse_int(name):
        value = request.query.get(name)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            raise web.HTTPBadRequest(
                text=json.dumps({"error": f"{name} must be integer"}),
                content_type="application/json",
            ) from None

    from_node = parse_int("from_node")
    to_node = parse_int("to_node")

    # -------- Case 1: NO FILTERS → return global totals --------
    no_filters = (
        period_type is None
        and length is None
        and channel is None
        and from_node is None
        and to_node is None
        and packet_id is None
    )

    if no_filters:
        total_packets = await store.get_total_packet_count()
        total_seen = await store.get_total_packet_seen_count()
        return web.json_response({"total_packets": total_packets, "total_seen": total_seen})

    # -------- Case 2: Apply filters → compute totals --------
    total_packets = await store.get_total_packet_count(
        period_type=period_type,
        length=length,
        channel=channel,
        from_node=from_node,
        to_node=to_node,
    )

    total_seen = await store.get_total_packet_seen_count(
        packet_id=packet_id,
        period_type=period_type,
        length=length,
        channel=channel,
        from_node=from_node,
        to_node=to_node,
    )

    return web.json_response({"total_packets": total_packets, "total_seen": total_seen})


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
            "chat": get_bool(site, "chat", True),
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

    # Get database file size
    try:
        db_url = CONFIG.get("database", {}).get("connection_string", "")
        # Extract file path from SQLite connection string (e.g., "sqlite+aiosqlite:///packets.db")
        if "sqlite" in db_url.lower():
            db_path = db_url.split("///")[-1].split("?")[0]
            if os.path.exists(db_path):
                db_size_bytes = os.path.getsize(db_path)
                # Convert to human-readable format
                if db_size_bytes < 1024:
                    health_status["database_size"] = f"{db_size_bytes} B"
                elif db_size_bytes < 1024 * 1024:
                    health_status["database_size"] = f"{db_size_bytes / 1024:.2f} KB"
                elif db_size_bytes < 1024 * 1024 * 1024:
                    health_status["database_size"] = f"{db_size_bytes / (1024 * 1024):.2f} MB"
                else:
                    health_status["database_size"] = (
                        f"{db_size_bytes / (1024 * 1024 * 1024):.2f} GB"
                    )
                health_status["database_size_bytes"] = db_size_bytes
    except Exception as e:
        logger.warning(f"Failed to get database size: {e}")
        # Don't fail health check if we can't get size

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


@routes.get("/api/packets_seen/{packet_id}")
async def api_packets_seen(request):
    try:
        # --- Validate packet_id ---
        try:
            packet_id = int(request.match_info["packet_id"])
        except (KeyError, ValueError):
            return web.json_response(
                {"error": "Invalid or missing packet_id"},
                status=400,
            )

        # --- Fetch list using your helper ---
        rows = await store.get_packets_seen(packet_id)

        items = []
        for row in rows:  # <-- FIX: normal for-loop
            items.append(
                {
                    "packet_id": row.packet_id,
                    "node_id": row.node_id,
                    "rx_time": row.rx_time,
                    "hop_limit": row.hop_limit,
                    "hop_start": row.hop_start,
                    "channel": row.channel,
                    "rx_snr": row.rx_snr,
                    "rx_rssi": row.rx_rssi,
                    "topic": row.topic,
                    "import_time": (row.import_time.isoformat() if row.import_time else None),
                    "import_time_us": row.import_time_us,
                }
            )

        return web.json_response({"seen": items})

    except Exception:
        logger.exception("Error in /api/packets_seen")
        return web.json_response(
            {"error": "Internal server error"},
            status=500,
        )
