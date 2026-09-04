"""Assemble node paths from Meshtastic RouteDiscovery payloads.

A traceroute response carries the endpoints reversed with respect to the path
being traced: `to` is the node that started the traceroute and `from` is the node
that answered. Only the response direction is affected, so both orientations are
handled here rather than at each call site.
"""

# Firmware inserts this into route[] as a placeholder for a hop it could not identify.
NODENUM_BROADCAST = 0xFFFFFFFF


def strip_unknown_hops(hops):
    return [hop for hop in hops if hop != NODENUM_BROADCAST]


def forward_path(from_node_id, to_node_id, hops, done, gateway_node_id=None):
    """Path towards the traced node, starting at the node that began the traceroute."""
    if done:
        return [node for node in (to_node_id, *hops, from_node_id) if node is not None]

    path = [node for node in (from_node_id, *hops) if node is not None]
    # Some nodes add themselves to the route before uplinking.
    if gateway_node_id is not None and (not path or path[-1] != gateway_node_id):
        path.append(gateway_node_id)
    return path


def return_path(from_node_id, to_node_id, hops):
    """Path back from the traced node, starting at the node that answered."""
    return [node for node in (from_node_id, *hops, to_node_id) if node is not None]


def endpoints(from_node_id, to_node_id, done):
    """The (initiator, target) of the traceroute, regardless of packet direction."""
    if done:
        return to_node_id, from_node_id
    return from_node_id, to_node_id
