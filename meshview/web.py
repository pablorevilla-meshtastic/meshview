import asyncio
import datetime
import logging
import os
import re
import ssl
from dataclasses import dataclass

import pydot
from aiohttp import web
from google.protobuf import text_format
from google.protobuf.message import Message
from jinja2 import Environment, PackageLoader, Undefined, select_autoescape
from markupsafe import Markup

from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import config, database, decode_payload, migrations, models, store
from meshview.__version__ import (
    __version_string__,
)
from meshview.web_api import api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d [pid:%(process)d] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
SEQ_REGEX = re.compile(r"seq \d+")
SOFTWARE_RELEASE = __version_string__  # Keep for backward compatibility
CONFIG = config.CONFIG

env = Environment(loader=PackageLoader("meshview"), autoescape=select_autoescape())

# Start Database
database.init_database(CONFIG["database"]["connection_string"])

BASE_DIR = os.path.dirname(__file__)
LANG_DIR = os.path.join(BASE_DIR, "lang")

with open(os.path.join(os.path.dirname(__file__), '1x1.png'), 'rb') as png:
    empty_png = png.read()


@dataclass
class Packet:
    id: int
    from_node_id: int
    from_node: models.Node
    to_node_id: int
    to_node: models.Node
    portnum: int
    data: str
    raw_mesh_packet: object
    raw_payload: object
    payload: str
    pretty_payload: Markup
    import_time: datetime.datetime
    import_time_us: int

    @classmethod
    def from_model(cls, packet):
        mesh_packet, payload = decode_payload.decode(packet)
        pretty_payload = None

        if mesh_packet:
            mesh_packet.decoded.payload = b""
            text_mesh_packet = text_format.MessageToString(mesh_packet)
        else:
            text_mesh_packet = "Did node decode"

        if payload is None:
            text_payload = "Did not decode"
        elif isinstance(payload, Message):
            text_payload = text_format.MessageToString(payload)
        elif packet.portnum == PortNum.TEXT_MESSAGE_APP and packet.to_node_id != 0xFFFFFFFF:
            text_payload = "<redacted>"
        elif isinstance(payload, bytes):
            text_payload = payload.decode("utf-8", errors="replace")  # decode bytes safely
        else:
            text_payload = str(payload)

        if payload:
            if (
                packet.portnum == PortNum.POSITION_APP
                and getattr(payload, "latitude_i", None)
                and getattr(payload, "longitude_i", None)
            ):
                pretty_payload = Markup(
                    f'<a href="https://www.google.com/maps/search/?api=1&query={payload.latitude_i * 1e-7},{payload.longitude_i * 1e-7}" target="_blank">map</a>'
                )

        return cls(
            id=packet.id,
            from_node=packet.from_node,
            from_node_id=packet.from_node_id,
            to_node=packet.to_node,
            to_node_id=packet.to_node_id,
            portnum=packet.portnum,
            data=text_mesh_packet,
            payload=text_payload,  # now always a string
            pretty_payload=pretty_payload,
            import_time=packet.import_time,
            import_time_us=packet.import_time_us,  # <-- include microseconds
            raw_mesh_packet=mesh_packet,
            raw_payload=payload,
        )


async def build_trace(node_id):
    trace = []
    for raw_p in await store.get_packets_from(
        node_id, PortNum.POSITION_APP, since=datetime.timedelta(hours=24)
    ):
        p = Packet.from_model(raw_p)
        if not p.raw_payload or not p.raw_payload.latitude_i or not p.raw_payload.longitude_i:
            continue
        trace.append((p.raw_payload.latitude_i * 1e-7, p.raw_payload.longitude_i * 1e-7))

    if not trace:
        for raw_p in await store.get_packets_from(node_id, PortNum.POSITION_APP):
            p = Packet.from_model(raw_p)
            if not p.raw_payload or not p.raw_payload.latitude_i or not p.raw_payload.longitude_i:
                continue
            trace.append((p.raw_payload.latitude_i * 1e-7, p.raw_payload.longitude_i * 1e-7))
            break

    return trace


async def build_neighbors(node_id):
    packets = await store.get_packets_from(node_id, PortNum.NEIGHBORINFO_APP, limit=1)
    packet = packets.first()

    if not packet:
        return []

    _, payload = decode_payload.decode(packet)
    neighbors = {}

    # Gather node information asynchronously
    tasks = {n.node_id: store.get_node(n.node_id) for n in payload.neighbors}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    for neighbor, node in zip(payload.neighbors, results, strict=False):
        if isinstance(node, Exception):
            continue
        if node and node.last_lat and node.last_long:
            neighbors[neighbor.node_id] = {
                'node_id': neighbor.node_id,
                'snr': neighbor.snr,  # Fix dictionary keying issue
                'short_name': node.short_name,
                'long_name': node.long_name,
                'location': (node.last_lat * 1e-7, node.last_long * 1e-7),
            }

    return list(neighbors.values())  # Return a list of dictionaries


def node_id_to_hex(node_id):
    if node_id is None or isinstance(node_id, Undefined):
        return "Invalid node_id"  # i... have no clue
    if node_id == 4294967295:
        return "^all"
    else:
        return f"!{hex(node_id)[2:].zfill(8)}"


def format_timestamp(timestamp):
    if isinstance(timestamp, int):
        timestamp = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
    return timestamp.isoformat(timespec="milliseconds")


env.filters["node_id_to_hex"] = node_id_to_hex
env.filters["format_timestamp"] = format_timestamp

# Initialize API module with dependencies
api.init_api_module(Packet, SEQ_REGEX, LANG_DIR)

# Create main routes table
routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    """
    Redirect root URL '/' to the page specified in CONFIG['site']['starting'].
    Defaults to '/map' if not set.
    """
    # Get the starting page from config
    starting_url = CONFIG["site"].get("starting", "/map")  # default to /map if not set
    raise web.HTTPFound(location=starting_url)


# redirect for backwards compatibility
@routes.get("/packet_list/{packet_id}")
async def redirect_packet_list(request):
    packet_id = request.match_info["packet_id"]
    raise web.HTTPFound(location=f"/node/{packet_id}")


@routes.get("/net")
async def net(request):
    return web.Response(
        text=env.get_template("net.html").render(),
        content_type="text/html",
    )


@routes.get("/map")
async def map(request):
    template = env.get_template("map.html")
    return web.Response(text=template.render(), content_type="text/html")


@routes.get("/nodelist")
async def nodelist(request):
    template = env.get_template("nodelist.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/firehose")
async def firehose(request):
    return web.Response(
        text=env.get_template("firehose.html").render(),
        content_type="text/html",
    )


@routes.get("/chat")
async def chat(request):
    template = env.get_template("chat.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/packet/{packet_id}")
async def new_packet(request):
    template = env.get_template("packet.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/node/{from_node_id}")
async def firehose_node(request):
    template = env.get_template("node.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/nodegraph")
async def nodegraph(request):
    template = env.get_template("nodegraph.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/top")
async def top(request):
    template = env.get_template("top.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


@routes.get("/stats")
async def stats(request):
    template = env.get_template("stats.html")
    return web.Response(
        text=template.render(),
        content_type="text/html",
    )


# Keep !!
@routes.get("/graph/traceroute/{packet_id}")
async def graph_traceroute(request):
    packet_id = int(request.match_info['packet_id'])
    traceroutes = list(await store.get_traceroute(packet_id))

    packet = await store.get_packet(packet_id)
    if not packet:
        return web.Response(
            status=404,
        )

    node_ids = set()
    for tr in traceroutes:
        route = decode_payload.decode_payload(PortNum.TRACEROUTE_APP, tr.route)
        node_ids.add(tr.gateway_node_id)
        for node_id in route.route:
            node_ids.add(node_id)
    node_ids.add(packet.from_node_id)
    node_ids.add(packet.to_node_id)

    nodes = {}
    async with asyncio.TaskGroup() as tg:
        for node_id in node_ids:
            nodes[node_id] = tg.create_task(store.get_node(node_id))

    graph = pydot.Dot('traceroute', graph_type="digraph")

    paths = set()
    node_color = {}
    mqtt_nodes = set()
    saw_reply = set()
    dest = None
    node_seen_time = {}
    for tr in traceroutes:
        if tr.done:
            saw_reply.add(tr.gateway_node_id)
        if tr.done and dest:
            continue
        route = decode_payload.decode_payload(PortNum.TRACEROUTE_APP, tr.route)
        path = [packet.from_node_id]
        path.extend(route.route)
        if tr.done:
            dest = packet.to_node_id
            path.append(packet.to_node_id)
        elif path[-1] != tr.gateway_node_id:
            # It seems some nodes add them self to the list before uplinking
            path.append(tr.gateway_node_id)

        if not tr.done and tr.gateway_node_id not in node_seen_time and tr.import_time:
            node_seen_time[path[-1]] = tr.import_time

        mqtt_nodes.add(tr.gateway_node_id)
        node_color[path[-1]] = '#' + hex(hash(tuple(path)))[3:9]
        paths.add(tuple(path))

    used_nodes = set()
    for path in paths:
        used_nodes.update(path)

    import_times = [tr.import_time for tr in traceroutes if tr.import_time]
    if import_times:
        first_time = min(import_times)
    else:
        first_time = 0

    for node_id in used_nodes:
        node = await nodes[node_id]
        if not node:
            node_name = node_id_to_hex(node_id)
        else:
            node_name = (
                f'[{node.short_name}] {node.long_name}\n{node_id_to_hex(node_id)}\n{node.role}'
            )
        if node_id in node_seen_time:
            ms = (node_seen_time[node_id] - first_time).total_seconds() * 1000
            node_name += f'\n {ms:.2f}ms'
        style = 'dashed'
        if node_id == dest:
            style = 'filled'
        elif node_id in mqtt_nodes:
            style = 'solid'

        if node_id in saw_reply:
            style += ', diagonals'

        graph.add_node(
            pydot.Node(
                str(node_id),
                label=node_name,
                shape='box',
                color=node_color.get(node_id, 'black'),
                style=style,
                href=f"/packet_list/{node_id}",
            )
        )

    for path in paths:
        color = '#' + hex(hash(tuple(path)))[3:9]
        for src, dest in zip(path, path[1:], strict=False):
            graph.add_edge(pydot.Edge(src, dest, color=color))

    return web.Response(
        body=graph.create_svg(),
        content_type="image/svg+xml",
    )


'''
@routes.get("/stats")
async def stats(request):
    try:
        total_packets = await store.get_total_packet_count()
        total_nodes = await store.get_total_node_count()
        total_packets_seen = await store.get_total_packet_seen_count()
        template = env.get_template("stats.html")
        return web.Response(
            text=template.render(
                total_packets=total_packets,
                total_nodes=total_nodes,
                total_packets_seen=total_packets_seen,
            ),
            content_type="text/html",
        )
    except Exception as e:
        return web.Response(
            text=f"An error occurred: {str(e)}",
            status=500,
            content_type="text/plain",
        )
'''


async def run_server():
    # Wait for database migrations to complete before starting web server
    logger.info("Checking database schema status...")
    database_url = CONFIG["database"]["connection_string"]

    # Wait for migrations to complete (writer app responsibility)
    migration_ready = await migrations.wait_for_migrations(
        database.engine, database_url, max_retries=30, retry_delay=2
    )

    if not migration_ready:
        logger.error("Database schema is not up to date. Cannot start web server.")
        raise RuntimeError("Database schema version mismatch - migrations not complete")

    logger.info("Database schema verified - starting web server")

    app = web.Application()
    app.add_routes(api.routes)  # Add API routes
    app.add_routes(routes)  # Add main web routes

    # Check if access logging should be disabled
    enable_access_log = CONFIG.get("logging", {}).get("access_log", "False").lower() == "true"
    access_log_handler = None if not enable_access_log else logging.getLogger("aiohttp.access")

    runner = web.AppRunner(app, access_log=access_log_handler)
    await runner.setup()
    if CONFIG["server"]["tls_cert"]:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(CONFIG["server"]["tls_cert"])
        logger.info(f"TLS enabled with certificate: {CONFIG['server']['tls_cert']}")
    else:
        ssl_context = None
        logger.info("TLS disabled")
    if host := CONFIG["server"]["bind"]:
        port = CONFIG["server"]["port"]
        protocol = "https" if ssl_context else "http"
        site = web.TCPSite(runner, host, port, ssl_context=ssl_context)
        await site.start()
        # Display localhost instead of wildcard addresses for usability
        display_host = "localhost" if host in ("0.0.0.0", "*", "::") else host
        logger.info(f"Web server started at {protocol}://{display_host}:{port}")
    while True:
        await asyncio.sleep(3600)  # sleep forever
