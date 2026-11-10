"""Node names are drawn as text in the traceroute graph; they cannot add to it or break it."""

import shutil
import xml.etree.ElementTree as ET
from types import SimpleNamespace

import pytest

from meshtastic.protobuf.mesh_pb2 import RouteDiscovery

pytestmark = pytest.mark.skipif(shutil.which("dot") is None, reason="Graphviz is not installed")

SVG = "{http://www.w3.org/2000/svg}"
HREF = "{http://www.w3.org/1999/xlink}href"
START, HOP, GATEWAY, TARGET = 1001, 1002, 1003, 1004

# (stored value, text the graph must show)
NAMES = [
    ("Bay Area Node", "Bay Area Node"),
    ("Ñandú 🪵 | bayme.sh", "Ñandú 🪵 | bayme.sh"),
    # A backslash before the quote used to end the label, so the rest became graph syntax.
    ('x\\" URL=<javascript:alert(1)>]; //', 'x\\" URL=<javascript:alert(1)>]; //'),
    ('x\\"]; 9999 [label=added]; 9999 -> 1001; //', 'x\\"]; 9999 [label=added]; 9999 -> 1001; //'),
    ('two \\\\" backslashes', 'two \\\\" backslashes'),
    ("ends with a backslash \\", "ends with a backslash \\"),
    # Graphviz replaces \N and \G with the node and graph name, and \l \r \n start a new line.
    ("\\N \\G \\E \\T \\L \\l \\r \\n", "\\N \\G \\E \\T \\L \\l \\r \\n"),
    ('"quoted"', '"quoted"'),
    ("<b>bold</b> & <i>more</i>", "<b>bold</b> & <i>more</i>"),
    # Graphviz stops reading at a NUL and the other control characters are not valid in SVG.
    ("a\x00b\x07c\x1bd\te\nf\rg\x7fh", "a b c d e f g h"),
    # Graphviz refuses a quoted string longer than 16384 bytes, so names are cut to 100.
    ("B" * 100, "B" * 100),
    ("C" * 101, "C" * 100),
    ("D" * 20000, "D" * 100),
    ("\\" * 9000, "\\" * 100),
]


async def draw(monkeypatch, nodes):
    """Run the real request handler for a route START -> HOP -> GATEWAY and parse its SVG."""
    from meshview import store, web

    row = SimpleNamespace(
        route=RouteDiscovery(route=[HOP]).SerializeToString(),
        done=False,
        gateway_node_id=GATEWAY,
        import_time_us=0,
    )

    async def get_traceroute(packet_id):
        return [row]

    async def get_packet(packet_id):
        return SimpleNamespace(from_node_id=START, to_node_id=TARGET)

    async def get_node(node_id):
        return nodes.get(node_id)

    monkeypatch.setattr(store, "get_traceroute", get_traceroute)
    monkeypatch.setattr(store, "get_packet", get_packet)
    monkeypatch.setattr(store, "get_node", get_node)
    response = await web.graph_traceroute(SimpleNamespace(match_info={"packet_id": "1"}))
    assert response.content_type == "image/svg+xml"

    drawn = {"nodes": {}, "edges": set(), "links": set()}
    for group in ET.fromstring(response.body).iter(f"{SVG}g"):
        title = group.findtext(f"{SVG}title")
        if group.get("class") == "node":
            drawn["nodes"][title] = [text.text for text in group.iter(f"{SVG}text")]
        elif group.get("class") == "edge":
            drawn["edges"].add(title)
        drawn["links"].update(a.get(HREF) for a in group.iter(f"{SVG}a"))
    return drawn


def node(short_name="ab", long_name="Plain", role="CLIENT"):
    return SimpleNamespace(short_name=short_name, long_name=long_name, role=role)


@pytest.mark.asyncio
@pytest.mark.parametrize(("stored", "shown"), NAMES)
async def test_names_are_drawn_as_text(monkeypatch, stored, shown):
    drawn = await draw(
        monkeypatch,
        {
            START: node(short_name=stored),
            HOP: node(long_name=stored),
            GATEWAY: node(role=stored),
        },
    )
    # Exactly the three nodes and two links of the route, each linking to its own node page.
    assert drawn["edges"] == {"1001->1002", "1002->1003"}
    assert drawn["links"] == {"/node/1001", "/node/1002", "/node/1003"}
    assert drawn["nodes"] == {
        "1001": [f"[{shown}] Plain", "!000003e9", "CLIENT"],
        "1002": [f"[ab] {shown}", "!000003ea", "CLIENT"],
        "1003": ["[ab] Plain", "!000003eb", shown],
    }


@pytest.mark.asyncio
async def test_unknown_nodes_are_drawn_by_id(monkeypatch):
    drawn = await draw(monkeypatch, {})
    assert drawn["edges"] == {"1001->1002", "1002->1003"}
    assert drawn["nodes"] == {"1001": ["!000003e9"], "1002": ["!000003ea"], "1003": ["!000003eb"]}
