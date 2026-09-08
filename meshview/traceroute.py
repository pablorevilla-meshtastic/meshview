"""Assemble node paths from Meshtastic RouteDiscovery payloads.

A traceroute response carries the endpoints reversed with respect to the path
being traced: `to` is the node that started the traceroute and `from` is the node
that answered. Only the response direction is affected, so both orientations are
handled here rather than at each call site.
"""

# Firmware inserts this into route[] as a placeholder for a hop it could not identify.
NODENUM_BROADCAST = 0xFFFFFFFF


def return_is_complete(route):
    """True when the response was seen after it reached the node that started it.

    Relays append both their ID and their SNR, but the final recipient appends only its
    SNR, so one spare SNR entry means the return trip finished. Gateways usually report
    a response that is still in flight, where the remaining hops are not known yet.
    """
    return len(route.snr_back) == len(route.route_back) + 1


def forward_path(from_node_id, to_node_id, hops, done, gateway_node_id=None):
    """Path towards the traced node, starting at the node that began the traceroute."""
    if done:
        return [node for node in (to_node_id, *hops, from_node_id) if node is not None]

    path = [node for node in (from_node_id, *hops) if node is not None]
    # Some nodes add themselves to the route before uplinking.
    if gateway_node_id is not None and (not path or path[-1] != gateway_node_id):
        path.append(gateway_node_id)
    return path


def return_path(from_node_id, to_node_id, hops, complete):
    """Path back from the traced node, starting at the node that answered."""
    path = [node for node in (from_node_id, *hops) if node is not None]
    if complete and to_node_id is not None:
        path.append(to_node_id)
    return path


def edges(path):
    """Consecutive pairs of a path, skipping links that run through an unknown hop."""
    for a, b in zip(path, path[1:], strict=False):
        if NODENUM_BROADCAST in (a, b):
            continue
        yield a, b


def endpoints(from_node_id, to_node_id, done):
    """The (initiator, target) of the traceroute, regardless of packet direction."""
    if done:
        return to_node_id, from_node_id
    return from_node_id, to_node_id
