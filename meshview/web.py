import asyncio
import datetime
import io
import json
import os
import re
import ssl
from collections import Counter
from dataclasses import dataclass
import matplotlib.pyplot as plt
import plotly.express as px
import psutil
import pydot
import seaborn as sns
from google.protobuf import text_format
from google.protobuf.message import Message
from jinja2 import Environment, PackageLoader, select_autoescape, Undefined
from markupsafe import Markup
from pandas import DataFrame
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import config
from meshview import database
from meshview import decode_payload
from meshview import models
from meshview import store
from meshview.store import get_total_node_count
from aiohttp import web
SOFTWARE_RELEASE= "2.0.1"
CONFIG = config.CONFIG

env = Environment(loader=PackageLoader("meshview"), autoescape=select_autoescape())
# Start Database
database.init_database(CONFIG["database"]["connection_string"])

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
        elif (
            packet.portnum == PortNum.TEXT_MESSAGE_APP
            and packet.to_node_id != 0xFFFFFFFF
        ):
            text_payload = "<redacted>"
        else:
            text_payload = payload

        if payload:
            if (
                packet.portnum == PortNum.POSITION_APP
                and payload.latitude_i
                and payload.longitude_i
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
            payload=text_payload,
            pretty_payload=pretty_payload,
            import_time=packet.import_time,
            raw_mesh_packet=mesh_packet,
            raw_payload=payload,
        )

@dataclass
class UplinkedNode:
    lat: float
    long: float
    long_name: str
    short_name: str
    hops: int
    snr: float
    rssi: float


async def build_trace(node_id):
    trace = []
    for raw_p in await store.get_packets_from(node_id, PortNum.POSITION_APP, since=datetime.timedelta(hours=24)):
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
    print(packet)
    if not packet:
        return []

    _, payload = decode_payload.decode(packet)
    neighbors = {}

    # Gather node information asynchronously
    tasks = {n.node_id: store.get_node(n.node_id) for n in payload.neighbors}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    for neighbor, node in zip(payload.neighbors, results):
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
        return "Invalid node_id" # i... have no clue
    if node_id == 4294967295:
        return "^all"
    else:
        return f"!{hex(node_id)[2:]}"


def format_timestamp(timestamp):
    if isinstance(timestamp, int):
        timestamp = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    return timestamp.isoformat(timespec="milliseconds")


env.filters["node_id_to_hex"] = node_id_to_hex
env.filters["format_timestamp"] = format_timestamp

routes = web.RouteTableDef()
# Make the Map the home page
@routes.get("/")
async def index(request):
    raise web.HTTPFound(location="/map")


def generate_response(request, body, raw_node_id="", node=None):
    if "HX-Request" in request.headers:
        return web.Response(text=body, content_type="text/html")

    template = env.get_template("index.html")
    response = web.Response(
        text=template.render(
            is_hx_request="HX-Request" in request.headers,
            raw_node_id=raw_node_id,
            node_html=Markup(body),
            node=node,
        ),
        content_type="text/html",
    )
    return response


@routes.get("/node_search")
async def node_search(request):
    if not "q" in request.query or not request.query["q"]:
        return web.Response(text="Bad node id")

    raw_node_id = request.query["q"]
    node_id = None

    if raw_node_id == "^all":
        node_id = 0xFFFFFFFF
    elif raw_node_id[0] == "!":
        try:
            node_id = int(raw_node_id[1:], 16)
        except ValueError:
            pass
    else:
        try:
            node_id = int(raw_node_id)
        except ValueError:
            pass

    if node_id is None:
        fuzzy_nodes = list(await store.get_fuzzy_nodes(raw_node_id))
        if len(fuzzy_nodes) == 1:
            node_id = fuzzy_nodes[0].node_id

    if node_id:
        return web.Response(
            status=307,
            headers={'Location': f'/packet_list/{node_id}?{request.query_string}'},
        )

    template = env.get_template("search.html")
    response = web.Response(
        text=template.render(nodes=fuzzy_nodes, query_string=request.query_string),
        content_type="text/html",
    )
    return response


@routes.get("/node_match")
async def node_match(request):
    if not "q" in request.query or not request.query["q"]:
        return web.Response(text="Bad node id")
    raw_node_id = request.query["q"]
    node_options = await store.get_fuzzy_nodes(raw_node_id)

    template = env.get_template("datalist.html")
    return web.Response(
        text=template.render(
            node_options=node_options,
            site_config = CONFIG

        ),
        content_type="text/html",
    )


@routes.get("/packet_list/{node_id}")
async def packet_list(request):
    node_id = int(request.match_info["node_id"])
    if portnum := request.query.get("portnum"):
        portnum = int(portnum)
    else:
        portnum = None

    async with asyncio.TaskGroup() as tg:
        node = tg.create_task(store.get_node(node_id))
        raw_packets = tg.create_task(store.get_packets(node_id,portnum, limit=200))
        trace = tg.create_task(build_trace(node_id))
        neighbors = await tg.create_task(build_neighbors(node_id))
        has_telemetry = tg.create_task(store.has_packets(node_id, PortNum.TELEMETRY_APP))

    packets = [Packet.from_model(p) for p in await raw_packets]  # Convert generator to a list
    template = env.get_template("node.html")
    return web.Response(
        text=template.render(
            raw_node_id=node_id_to_hex(node_id),
            node_id=node_id,
            node=await node,
            portnum=portnum,
            packets=packets,
            trace=await trace,
            neighbors=neighbors,
            has_telemetry=await has_telemetry,
            query_string=request.query_string,
            site_config = CONFIG,
        ),
        content_type="text/html",
    )


@routes.get("/packet_list_text/{node_id}")
async def packet_list_text(request):
    node_id = int(request.match_info["node_id"])
    portnum = int(request.query.get("portnum")) if request.query.get("portnum") else None

    async with asyncio.TaskGroup() as tg:
        raw_packets = tg.create_task(store.get_packets(node_id, portnum, limit=200))

    packets = [Packet.from_model(p) for p in await raw_packets]  # Convert generator to a list

    # Convert packets to a plain text format with formatted import time and raw payload
    text_data = "\n\n----------------------\n\n".join(
        f"{packet.import_time.strftime('%-I:%M:%S %p - %m-%d-%Y')}\n{packet.raw_payload}"
        for packet in packets
    )

    return web.Response(
        text=text_data,
        content_type="text/plain",
    )


# Updated code p.r.
@routes.get("/packet_details/{packet_id}")
async def packet_details(request):
    packet_id = int(request.match_info["packet_id"])
    packets_seen = list(await store.get_packets_seen(packet_id))
    packet = await store.get_packet(packet_id)

    node = None
    if packet and packet.from_node_id:
        node = await store.get_node(packet.from_node_id)

    from_node_cord = None
    if packet and packet.from_node and packet.from_node.last_lat:
        from_node_cord = [
            packet.from_node.last_lat * 1e-7,
            packet.from_node.last_long * 1e-7,
        ]

    uplinked_nodes = []
    for p in packets_seen:
        if p.node and p.node.last_lat:
            if p.topic.startswith('mqtt-meshtastic-org'):
                hops = 666
            else:
                hops = p.hop_start - p.hop_limit
            uplinked_nodes.append(
                UplinkedNode(
                    lat=p.node.last_lat * 1e-7,
                    long=p.node.last_long * 1e-7,
                    long_name=p.node.long_name,
                    short_name=p.node.short_name,
                    hops=hops,
                    snr=p.rx_snr,
                    rssi=p.rx_rssi,
                )
            )

    map_center = None
    if from_node_cord:
        map_center = from_node_cord
    elif uplinked_nodes:
        map_center = [uplinked_nodes[0].lat, uplinked_nodes[0].long]

    # Render the template and return the response
    template = env.get_template("packet_details.html")
    return web.Response(
        text=template.render(
            packets_seen=packets_seen,
            map_center=map_center,
            from_node_cord=from_node_cord,
            uplinked_nodes=uplinked_nodes,
            node=node,
            site_config = CONFIG,
        ),
        content_type="text/html",
    )


@routes.get("/firehose")
async def packet_details(request):
    portnum = request.query.get("portnum")
    if portnum:
        portnum = int(portnum)
    packets = await store.get_packets(portnum=portnum, limit=20)
    print_memory_usage()
    template = env.get_template("firehose.html")
    return web.Response(
        text=template.render(
            packets=(Packet.from_model(p) for p in packets),
            portnum=portnum,
            site_config = CONFIG,
        ),
        content_type="text/html",
    )


@routes.get("/packet/{packet_id}")
async def packet(request):
    packet = await store.get_packet(int(request.match_info["packet_id"]))
    if not packet:
        return web.Response(status=404)

    node = await store.get_node(packet.from_node_id)
    print_memory_usage()
    template = env.get_template("packet_index.html")

    return web.Response(
        text=template.render(packet=Packet.from_model(packet), site_config = CONFIG),
        content_type="text/html",
    )



async def graph_telemetry(node_id, payload_type, graph_config):
    data = {'date': []}
    fields = []
    for c in graph_config:
        fields.extend(c['fields'])

    for field in fields:
        data[field] = []

    for p in await store.get_packets_from(node_id, PortNum.TELEMETRY_APP):
        _, payload = decode_payload.decode(p)
        if not payload:
            continue
        if not payload.HasField(payload_type):
            continue
        data_field = getattr(payload, payload_type)
        timestamp = p.import_time
        data['date'].append(timestamp)
        for field in fields:
            data[field].append(getattr(data_field, field))

    if not data['date']:
        return web.Response(
            body=empty_png,
            status=404,
            content_type="image/png",
        )

    max_time = datetime.timedelta(days=4)
    newest = data['date'][0]
    for i, d in enumerate(data['date']):
        if d < newest - max_time:
            break

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.autofmt_xdate()
    ax.set_xlabel('time')
    axes = {0: ax}

    date = data.pop('date')
    df = DataFrame(data, index=date)

    for i, ax_config in enumerate(graph_config):
        args = {}
        if 'color' in ax_config:
            args['color'] =  'tab:' + ax_config['color']
        if i:
            ax = ax.twinx()
        ax.set_ylabel(ax_config['label'], **args)
        ax_df = df[ax_config['fields']]
        args = {}
        if 'palette' in ax_config:
            args['palette'] = ax_config['palette']
        sns.lineplot(data=ax_df, ax=ax, **args)

    png = io.BytesIO()
    plt.savefig(png, dpi=100)
    plt.close()

    return web.Response(
        body=png.getvalue(),
        content_type="image/png",
    )



@routes.get("/graph/power/{node_id}")
async def graph_power(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'device_metrics',
        [
            {
                'label': 'battery level',
                'fields': ['battery_level'],
            },
            {
                'label': 'voltage',
                'fields': ['voltage'],
                'palette': 'Set2',
            },
        ],
    )


@routes.get("/graph/chutil/{node_id}")
async def graph_chutil(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'device_metrics',
        [
            {
                'label': 'utilization',
                'fields': ['channel_utilization', 'air_util_tx'],
            },
        ],
    )

@routes.get("/graph/wind_speed/{node_id}")
async def graph_wind_speed(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'wind speed m/s',
                'fields': ['wind_speed'],
            },
        ],
    )


@routes.get("/graph/wind_direction/{node_id}")
async def graph_wind_direction(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'wind direction',
                'fields': ['wind_direction'],
            },
        ],
    )

@routes.get("/graph/temperature/{node_id}")
async def graph_temperature(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'temperature C',
                'fields': ['temperature'],
            },
        ],
    )


@routes.get("/graph/humidity/{node_id}")
async def graph_humidity(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'humidity',
                'fields': ['relative_humidity'],
            },
        ],
    )

@routes.get("/graph/pressure/{node_id}")
async def graph_pressure(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'barometric pressure',
                'fields': ['barometric_pressure'],
            },
        ],
    )

@routes.get("/graph/iaq/{node_id}")
async def graph_pressure(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'environment_metrics',
        [
            {
                'label': 'IAQ',
                'fields': ['iaq'],
            },
        ],
    )

@routes.get("/graph/power_metrics/{node_id}")
async def graph_power_metrics(request):
    return await graph_telemetry(
        int(request.match_info['node_id']),
        'power_metrics',
        [
            {
                'label': 'voltage',
                'fields': ['ch1_voltage', 'ch2_voltage', 'ch3_voltage'],
            },
            {
                'label': 'current',
                'fields': ['ch1_current', 'ch2_current', 'ch3_current'],
                'palette': 'Set2',
            },
        ],
    )


@routes.get("/graph/neighbors/{node_id}")
async def graph_neighbors(request):
    oldest = datetime.datetime.now() - datetime.timedelta(days=4)

    data = {}
    dates =[]
    for p in await store.get_packets_from(int(request.match_info['node_id']), PortNum.NEIGHBORINFO_APP):
        _, payload = decode_payload.decode(p)
        if not payload:
            continue
        if p.import_time < oldest:
            break

        dates.append(p.import_time)
        for v in data.values():
            v.append(None)

        for n in payload.neighbors:
            data.setdefault(n.node_id, [None] * len(dates))[-1] = n.snr

    nodes = {}
    async with asyncio.TaskGroup() as tg:
        for node_id in data:
            nodes[node_id] = tg.create_task(store.get_node(node_id))

    data_by_short_name = {}
    for node_id, data in data.items():
        node = await nodes[node_id]
        if node:
            data_by_short_name[node.short_name] = data
        else:
            data_by_short_name[node_id_to_hex(node_id)] = data

    fig, ax1 = plt.subplots(figsize=(5, 5))
    ax1.set_xlabel('time')
    ax1.set_ylabel('SNR')
    df = DataFrame(data_by_short_name, index=dates)
    sns.lineplot(data=df)

    png = io.BytesIO()
    plt.savefig(png, dpi=100)
    plt.close()
    return web.Response(
        body=png.getvalue(),
        content_type="image/png",
    )

@routes.get("/graph/neighbors2/{node_id}")
async def graph_neighbors2(request):
    oldest = datetime.datetime.now() - datetime.timedelta(days=30)

    data = []
    node_ids = set()
    for p in await store.get_packets_from(int(request.match_info['node_id']), PortNum.NEIGHBORINFO_APP):
        _, payload = decode_payload.decode(p)
        if not payload:
            continue
        if p.import_time < oldest:
            break

        for n in payload.neighbors:
            node_ids.add(n.node_id)
            data.append({
                'time': p.import_time,
                'snr': n.snr,
                'node_id': n.node_id,
            })

    nodes = {}
    async with asyncio.TaskGroup() as tg:
        for node_id in node_ids:
            nodes[node_id] = tg.create_task(store.get_node(node_id))

    for d in data:
        node = await nodes[d['node_id']]
        if node:
            d['node_name'] = node.short_name
        else:
            d['node_name'] = node_id_to_hex(node_id)

    df = DataFrame(data)
    fig = px.line(df, x="time", y="snr", color="node_name", markers=True)
    html = fig.to_html(full_html=True, include_plotlyjs='cdn')
    print_memory_usage()
    return web.Response(
        text=html,
        content_type="text/html",
    )

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
            node_name = f'[{node.short_name}] {node.long_name}\n{node_id_to_hex(node_id)}\n{node.role}'
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

        graph.add_node(pydot.Node(
            str(node_id),
            label=node_name,
            shape='box',
            color=node_color.get(node_id, 'black'),
            style=style,
            href=f"/packet_list/{node_id}",
        ))

    for path in paths:
        color = '#' + hex(hash(tuple(path)))[3:9]
        for src, dest in zip(path, path[1:]):
            graph.add_edge(pydot.Edge(src, dest, color=color))

    return web.Response(
        body=graph.create_svg(),
        content_type="image/svg+xml",
    )


@routes.get("/graph/traceroute2/{packet_id}")
async def graph_traceroute2(request):
    packet_id = int(request.match_info['packet_id'])
    traceroutes = list(await store.get_traceroute(packet_id))

    # Fetch the packet
    packet = await store.get_packet(packet_id)
    if not packet:
        return web.Response(status=404)

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

    # Initialize graph for traceroute
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

    # Prepare data for ECharts rendering
    chart_nodes = []
    chart_edges = []
    for node_id in used_nodes:
        node = await nodes[node_id]
        if not node:
            # Handle case where node is None
            node_name = node_id_to_hex(node_id)
            chart_nodes.append({
                "name": str(node_id),
                "value": node_name,
                "symbol": 'rect',
            })
        else:
            node_name = f'[{node.short_name}] {node.long_name}\n{node_id_to_hex(node_id)}\n{node.role}'
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

            chart_nodes.append({
                "name": str(node_id),
                "value": node_name,
                "symbol": 'rect',
                "long_name": node.long_name,
                "short_name": node.short_name,
                "role": node.role,
                "hw_model": node.hw_model,
            })

    # Create edges
    for path in paths:
        color = '#' + hex(hash(tuple(path)))[3:9]
        for src, dest in zip(path, path[1:]):
            chart_edges.append({
                "source": str(src),
                "target": str(dest),
                "originalColor": color,
            })

    chart_data = {
        "nodes": chart_nodes,
        "edges": chart_edges,
    }

    template = env.get_template("traceroute.html")
    # Render the page with the chart data
    return web.Response(
        text=template.render(chart_data=chart_data, packet_id=packet_id),
        content_type="text/html",
    )



@routes.get("/graph/network")
async def graph_network(request):
    root = request.query.get("root")
    depth = int(request.query.get("depth", 5))
    hours = int(request.query.get("hours", 24))
    minutes = int(request.query.get("minutes", 0))
    since = datetime.timedelta(hours=hours, minutes=minutes)

    nodes = {}
    node_ids = set()

    traceroutes = []
    for tr in await store.get_traceroutes(since):
        node_ids.add(tr.gateway_node_id)
        node_ids.add(tr.packet.from_node_id)
        node_ids.add(tr.packet.to_node_id)
        route = decode_payload.decode_payload(PortNum.TRACEROUTE_APP, tr.route)
        node_ids.update(route.route)

        path = [tr.packet.from_node_id]
        path.extend(route.route)
        if tr.done:
            path.append(tr.packet.to_node_id)
        else:
            if path[-1] != tr.gateway_node_id:
                # It seems some nodes add them self to the list before uplinking
                path.append(tr.gateway_node_id)
        traceroutes.append((tr, path))

    edges = Counter()
    edge_type = {}
    used_nodes = set()

    for ps, p in await store.get_mqtt_neighbors(since):
        node_ids.add(ps.node_id)
        node_ids.add(p.from_node_id)
        used_nodes.add(ps.node_id)
        used_nodes.add(p.from_node_id)
        edges[(p.from_node_id, ps.node_id)] += 1
        edge_type[(p.from_node_id, ps.node_id)] = 'sni'

    for packet in await store.get_packets(
        portnum=PortNum.NEIGHBORINFO_APP,
        since=since,
    ):
        _, neighbor_info = decode_payload.decode(packet)
        node_ids.add(packet.from_node_id)
        used_nodes.add(packet.from_node_id)
        for node in neighbor_info.neighbors:
            node_ids.add(node.node_id)
            used_nodes.add(node.node_id)
            edges[(node.node_id, packet.from_node_id)] += 1
            edge_type[(node.node_id, packet.from_node_id)] = 'ni'

    async with asyncio.TaskGroup() as tg:
        for node_id in node_ids:
            nodes[node_id] = tg.create_task(store.get_node(node_id))

    tr_done = set()
    for tr, path in traceroutes:
        if tr.done:
            if tr.packet_id in tr_done:
                continue
            else:
                tr_done.add(tr.packet_id)

        for src, dest in zip(path, path[1:]):
            used_nodes.add(src)
            used_nodes.add(dest)
            edges[(src, dest)] += 1
            edge_type[(src, dest)] = 'tr'

    async def get_node_name(node_id):
        node = await nodes[node_id]
        if not node:
            node_name = node_id_to_hex(node_id)
        else:
            node_name = f'[{node.short_name}] {node.long_name}\n{node_id_to_hex(node_id)}'
        return node_name

    if root:
        new_used_nodes = set()
        new_edges = Counter()
        edge_map = {}
        for src, dest in edges:
            edge_map.setdefault(dest, []).append(src)

        queue = [int(root)]
        for i in range(depth):
            next_queue = []
            for node in queue:
                new_used_nodes.add(node)
                for dest in edge_map.get(node, []):
                    new_used_nodes.add(dest)
                    new_edges[(dest, node)] += 1
                    next_queue.append(dest)
            queue = next_queue

        used_nodes = new_used_nodes
        edges = new_edges
    # Create the graph
    graph = pydot.Dot('network', graph_type="digraph", layout="sfdp", overlap="prism", esep="+10", nodesep="0.5",
                      ranksep="1")

    for node_id in used_nodes:
        node = await nodes[node_id]
        color = '#000000'
        node_name = await get_node_name(node_id)
        if node and node.role in ('ROUTER', 'ROUTER_CLIENT', 'REPEATER'):
            color = '#0000FF'
        elif node and node.role == 'CLIENT_MUTE':
            color = '#00FF00'
        graph.add_node(pydot.Node(
            str(node_id),
            label=node_name,
            shape='box',
            color=color,
            href=f"/graph/network?root={node_id}&amp;depth={depth-1}",
        ))

    if edges:
        max_edge_count = edges.most_common(1)[0][1]
    else:
        max_edge_count = 1

    size_ratio = 2. / max_edge_count


    edge_added = set()

    for (src, dest), edge_count in edges.items():
        size = max(size_ratio * edge_count, .25)
        arrowsize = max(size_ratio * edge_count, .5)
        if edge_type[(src, dest)] in ('ni'):
            color = '#FF0000'
        elif  edge_type[(src, dest)] in ('sni'):
            color = '#00FF00'
        else:
            color = '#000000'
        edge_dir = "forward"
        if (dest, src) in edges and edge_type[(src, dest)] == edge_type[(dest, src)]:
            edge_dir = "both"
            edge_added.add((dest, src))

        if (src, dest) not in edge_added:
            edge_added.add((src, dest))
            graph.add_edge(pydot.Edge(
                str(src),
                str(dest),
                color=color,
                tooltip=f'{await get_node_name(src)} -> {await get_node_name(dest)}',
                penwidth=1.85,
                dir=edge_dir,
            ))
    print_memory_usage()
    return web.Response(
        body=graph.create_svg(),
        content_type="image/svg+xml",
    )



@routes.get("/nodelist")
async def nodelist(request):
    try:
        role = request.query.get("role")
        #print(role)
        channel = request.query.get("channel")
        #print(channel)
        hw_model = request.query.get("hw_model")
        #print(hw_model)
        nodes= await store.get_nodes(role,channel, hw_model, days_active=3)
        template = env.get_template("nodelist.html")
        return web.Response(
            text=template.render(nodes=nodes, site_config = CONFIG),
            content_type="text/html",
        )
    except Exception as e:

        return web.Response(
            text="An error occurred while processing your request.",
            status=500,
            content_type="text/plain",
        )


@routes.get("/api")
async def api(request):
    try:
        role = request.query.get("role")
        channel = request.query.get("channel")
        hw_model = request.query.get("hw_model")

        nodes = await store.get_nodes(role, channel, hw_model)

        nodes_json = [node.to_dict() for node in nodes]
        return web.json_response({"nodes": nodes_json})

    except Exception as e:
        import traceback
        print("Error in /api endpoint:", str(e))
        print(traceback.format_exc())
        return web.Response(
            text=f"An error occurred: {str(e)}",
            status=500,
            content_type="text/plain",
        )


@routes.get("/net")
async def net(request):
    try:
        print_memory_usage()
        # Fetch packets for the given node ID and port number
        packets = await store.get_packets(
            node_id=0xFFFFFFFF, portnum=PortNum.TEXT_MESSAGE_APP, limit=1000
        )

        # Convert packets to UI packets
        ui_packets = [Packet.from_model(p) for p in packets]

        # Precompile regex for performance
        seq_pattern = re.compile(r"seq \d+$")

        # Filter packets: exclude "seq \d+$" but include those containing Tag
        filtered_packets = [
            p for p in ui_packets
            if not seq_pattern.match(p.payload) and (CONFIG["site"]["net_tag"]).lower() in p.payload.lower()
        ]

        # Render template
        template = env.get_template("net.html")
        return web.Response(
            text=template.render(packets=filtered_packets, site_config = CONFIG),
            content_type="text/html",
        )

    except web.HTTPException as e:
        raise  # Let aiohttp handle HTTP exceptions properly

    except Exception as e:
        print("Error processing net request")
        return web.Response(
            text="An internal server error occurred.",
            status=500,
            content_type="text/plain",
        )


@routes.get("/map")
async def map(request):
    try:
        nodes = await store.get_nodes(days_active=3)

        # Filter out nodes with no latitude
        nodes = [node for node in nodes if node.last_lat is not None]

        # Optional datetime formatting
        for node in nodes:
            if hasattr(node, "last_update") and isinstance(node.last_update, datetime.datetime):
                node.last_update = node.last_update.isoformat()
        template = env.get_template("map.html")

        return web.Response(
            text=template.render(nodes=nodes, site_config=CONFIG),
            content_type="text/html",
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return web.Response(
            text="An error occurred while processing your request.",
            status=500,
            content_type="text/plain",
        )



# Print memory usage
def print_memory_usage():
    process = psutil.Process(os.getpid())
    print(f"Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")

@routes.get("/stats")
async def stats(request):
    try:
        total_packets = await store.get_total_packet_count()
        total_nodes = await store.get_total_node_count()
        total_packets_seen = await store.get_total_packet_seen_count()
        total_nodes_longfast = await get_total_node_count("LongFast")
        total_nodes_mediumslow = await get_total_node_count("MediumSlow")
        print_memory_usage()
        template = env.get_template("stats.html")
        return web.Response(
            text=template.render(
                total_packets=total_packets,
                total_nodes=total_nodes,
                total_packets_seen=total_packets_seen,
                total_nodes_longfast=total_nodes_longfast,
                total_nodes_mediumslow=total_nodes_mediumslow,
                site_config = CONFIG,
            ),
            content_type="text/html",
        )
    except Exception as e:
        return web.Response(
            text=f"An error occurred: {str(e)}",
            status=500,
            content_type="text/plain",
        )

@routes.get("/top")
async def top(request):
    try:
        node_id = request.query.get("node_id")  # Get node_id from the URL query parameters

        if node_id:
            # If node_id is provided, fetch traffic data for the specific node
            node_traffic = await store.get_node_traffic(int(node_id))
            template = env.get_template("node_traffic.html")  # Render a different template
            html_content = template.render(traffic=node_traffic, node_id=node_id, site_config = CONFIG)
        else:
            # Otherwise, fetch top traffic nodes as usual
            top_nodes = await store.get_top_traffic_nodes()
            template = env.get_template("top.html")
            html_content = template.render(nodes=top_nodes, site_config = CONFIG)

        return web.Response(
            text=html_content,
            content_type="text/html",
        )
    except Exception as e:
        return web.Response(
            text=f"An error occurred: {str(e)}",
            status=500,
            content_type="text/plain",
        )

@routes.get("/chat")
async def chat(request):
    try:
        packets = await store.get_packets(
            node_id=0xFFFFFFFF, portnum=PortNum.TEXT_MESSAGE_APP, limit=100
        )

        ui_packets = [Packet.from_model(p) for p in packets]
        filtered_packets = [
            p for p in ui_packets if not re.fullmatch(r"seq \d+", p.payload)
        ]
        #print("Example packet:", filtered_packets)
        template = env.get_template("chat.html")
        return web.Response(
            text=template.render(packets=filtered_packets, site_config=CONFIG),
            content_type="text/html",
        )
    except Exception as e:
        print("Error in /chat:", e)
        return web.Response(
            text="An error occurred while processing your request.",
            status=500,
            content_type="text/plain",
        )

# Assuming the route URL structure is /nodegraph
@routes.get("/nodegraph")
async def nodegraph(request):
    nodes = await store.get_nodes(days_active=3)  # Fetch nodes for the given channel
    node_ids = set()
    edges_set = set()  # Track unique edges
    edge_type = {}  # Store type of each edge
    used_nodes = set()  # This will track nodes involved in edges (including traceroutes)
    since = datetime.timedelta(hours=48)
    traceroutes = []

    # Fetch traceroutes
    for tr in await store.get_traceroutes(since):
        node_ids.add(tr.gateway_node_id)
        node_ids.add(tr.packet.from_node_id)
        node_ids.add(tr.packet.to_node_id)
        route = decode_payload.decode_payload(PortNum.TRACEROUTE_APP, tr.route)
        node_ids.update(route.route)

        path = [tr.packet.from_node_id]
        path.extend(route.route)
        if tr.done:
            path.append(tr.packet.to_node_id)
        else:
            if path[-1] != tr.gateway_node_id:
                path.append(tr.gateway_node_id)
        traceroutes.append((tr, path))

        # Add traceroute edges with their type and update used_nodes
        for i in range(len(path) - 1):
            edge_pair = (path[i], path[i + 1])
            edges_set.add(edge_pair)
            edge_type[edge_pair] = "traceroute"
            used_nodes.add(path[i])  # Add all nodes in the traceroute path
            used_nodes.add(path[i + 1])  # Add all nodes in the traceroute path

    # Fetch NeighborInfo packets
    for packet in await store.get_packets(portnum=PortNum.NEIGHBORINFO_APP, since=since):
        try:
            _, neighbor_info = decode_payload.decode(packet)
            node_ids.add(packet.from_node_id)
            used_nodes.add(packet.from_node_id)
            for node in neighbor_info.neighbors:
                node_ids.add(node.node_id)
                used_nodes.add(node.node_id)

                edge_pair = (node.node_id, packet.from_node_id)
                if edge_pair not in edges_set:
                    edges_set.add(edge_pair)
                    edge_type[edge_pair] = "neighbor"
        except Exception as e:
            print(f"Error decoding NeighborInfo packet: {e}")

    # Convert edges_set to a list of dicts with colors
    edges = [
        {
            "from": frm,
            "to": to,
            "originalColor": "#ff5733" if edge_type[(frm, to)] == "traceroute" else "#3388ff",  # Red for traceroute, Blue for neighbor
            "lineStyle": {
                "color": "#ff5733" if edge_type[(frm, to)] == "traceroute" else "#3388ff",
                "width": 2
            }
        }
        for frm, to in edges_set
    ]

    # Filter nodes to only include those involved in edges (including traceroutes)
    nodes_with_edges = [node for node in nodes if node.node_id in used_nodes]

    template = env.get_template("nodegraph.html")
    return web.Response(
        text=template.render(
            nodes=nodes_with_edges,
            edges=edges,  # Pass edges with color info
            site_config = CONFIG,
        ),
        content_type="text/html",
    )

# Show basic details about the site on the site
@routes.get("/config")
async def get_config(request):
    try:
        site = CONFIG.get("site", {})
        mqtt = CONFIG.get("mqtt", {})

        return web.json_response({
            "Server": site.get("domain", ""),
            "Title": site.get("title", ""),
            "Message": site.get("message", ""),
            "Topics": json.loads(mqtt.get("topics", "[]")),
            "Release": SOFTWARE_RELEASE
        })
    except (json.JSONDecodeError, TypeError):
        return web.json_response({"error": "Invalid configuration format"}, status=500)


async def run_server():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    if CONFIG["server"]["tls_cert"]:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(CONFIG["server"]["tls_cert"])
    else:
        ssl_context = None
    if host := CONFIG["server"]["bind"]:
        site = web.TCPSite(runner, host, CONFIG["server"]["port"], ssl_context=ssl_context)
        await site.start()
    while True:
        await asyncio.sleep(3600)  # sleep forever

