# API Documentation

Base URL: `http(s)://<host>`

All endpoints return JSON. Timestamps are either ISO 8601 strings or `*_us` values in
microseconds since epoch.

## 1. Nodes API

### GET `/api/nodes`
Returns a list of nodes, with optional filtering.

Query Parameters
- `node_id` (optional, int): Exact node ID.
- `role` (optional, string): Node role.
- `channel` (optional, string): Channel name.
- `hw_model` (optional, string): Hardware model.
- `days_active` (optional, int): Nodes seen within the last N days.

Response Example
```json
{
  "nodes": [
    {
      "id": 42,
      "node_id": 1234,
      "long_name": "Alice",
      "short_name": "A",
      "hw_model": "T-Beam",
      "firmware": "1.2.3",
      "role": "client",
      "last_lat": 377749000,
      "last_long": -1224194000,
      "channel": "main",
      "last_seen_us": 1736370123456789
    }
  ]
}
```

---

## 2. Packets API

### GET `/api/packets`
Returns packets with optional filters.

Query Parameters
- `packet_id` (optional, int): Return exactly one packet (overrides other filters).
- `limit` (optional, int): Max packets to return, clamped 1-1000. Default: `50`.
- `since` (optional, int): Only packets imported after this microsecond timestamp.
- `portnum` (optional, int): Filter by port number.
- `contains` (optional, string): Payload substring filter.
- `from_node_id` (optional, int): Filter by sender node ID.
- `to_node_id` (optional, int): Filter by recipient node ID.
- `node_id` (optional, int): Legacy filter matching either from or to node ID.

Response Example
```json
{
  "packets": [
    {
      "id": 123,
      "import_time_us": 1736370123456789,
      "channel": "main",
      "from_node_id": 5678,
      "to_node_id": 91011,
      "portnum": 1,
      "long_name": "Alice",
      "payload": "Hello, Bob!",
      "to_long_name": "Bob",
      "reply_id": 122
    }
  ],
  "latest_import_time": 1736370123456789
}
```

Notes
- For `portnum=1` (text messages), packets are filtered to remove sequence-only payloads.
- `latest_import_time` is returned when available for incremental polling (microseconds).

---

## 3. Channels API

### GET `/api/channels`
Returns channels seen in a time period.

Query Parameters
- `period_type` (optional, string): `hour` or `day`. Default: `hour`.
- `length` (optional, int): Number of periods to look back. Default: `24`.

Response Example
```json
{
  "channels": ["LongFast", "MediumFast", "ShortFast"]
}
```

---

## 4. Stats API

### GET `/api/stats`
Returns packet statistics aggregated by time periods, with optional filtering.

Query Parameters
- `period_type` (optional, string): `hour` or `day`. Default: `hour`.
- `length` (optional, int): Number of periods to include. Default: `24`.
- `channel` (optional, string): Filter by channel (case-insensitive).
- `portnum` (optional, int): Filter by port number.
- `to_node` (optional, int): Filter by destination node ID.
- `from_node` (optional, int): Filter by source node ID.
- `node` (optional, int): If provided, return combined `sent` and `seen` totals for that node.

Response Example (series)
```json
{
  "period_type": "hour",
  "length": 24,
  "channel": "LongFast",
  "portnum": 1,
  "to_node": 12345678,
  "from_node": 87654321,
  "data": [
    { "period": "2025-08-08 14:00", "count": 10 },
    { "period": "2025-08-08 15:00", "count": 7 }
  ]
}
```

Response Example (`node` totals)
```json
{
  "node_id": 12345678,
  "period_type": "hour",
  "length": 24,
  "sent": 42,
  "seen": 58
}
```

---

### GET `/api/stats/count`
Returns total packet counts, optionally filtered.

Query Parameters
- `packet_id` (optional, int): Filter packet_seen by packet ID.
- `period_type` (optional, string): `hour` or `day`.
- `length` (optional, int): Number of periods to include.
- `channel` (optional, string): Filter by channel.
- `from_node` (optional, int): Filter by source node ID.
- `to_node` (optional, int): Filter by destination node ID.

Response Example
```json
{
  "total_packets": 12345,
  "total_seen": 67890
}
```

---

### GET `/api/stats/top`
Returns nodes sorted by packets seen, with pagination.

Query Parameters
- `period_type` (optional, string): `hour` or `day`. Default: `day`.
- `length` (optional, int): Number of periods to include. Default: `1`.
- `channel` (optional, string): Filter by channel.
- `limit` (optional, int): Max nodes to return. Default: `20`, max `100`.
- `offset` (optional, int): Pagination offset. Default: `0`.

Response Example
```json
{
  "total": 250,
  "limit": 20,
  "offset": 0,
  "nodes": [
    {
      "node_id": 1234,
      "long_name": "Alice",
      "short_name": "A",
      "channel": "main",
      "sent": 100,
      "seen": 240,
      "avg": 2.4
    }
  ]
}
```

---

## 5. Edges API

### GET `/api/edges`
Returns network edges (connections between nodes) based on traceroutes and neighbor info.
Traceroute edges are collected over the last 12 hours. Neighbor edges are based on
port 71 packets.

Query Parameters
- `type` (optional, string): `traceroute` or `neighbor`. If omitted, returns both.
- `node_id` (optional, int): Filter edges to only those touching a node.

Response Example
```json
{
  "edges": [
    { "from": 12345678, "to": 87654321, "type": "traceroute" },
    { "from": 11111111, "to": 22222222, "type": "neighbor" }
  ]
}
```

---

## 6. Config API

### GET `/api/config`
Returns a safe subset of server configuration.

Response Example
```json
{
  "site": {
    "domain": "example.com",
    "language": "en",
    "title": "Meshview",
    "message": "",
    "starting": "/chat",
    "nodes": "true",
    "chat": "true",
    "everything": "true",
    "graphs": "true",
    "stats": "true",
    "net": "true",
    "map": "true",
    "top": "true",
    "map_top_left_lat": 39.0,
    "map_top_left_lon": -123.0,
    "map_bottom_right_lat": 36.0,
    "map_bottom_right_lon": -121.0,
    "map_interval": 3,
    "firehose_interval": 3,
    "weekly_net_message": "Weekly Mesh check-in message.",
    "net_tag": "#BayMeshNet",
    "version": "3.0.0"
  },
  "mqtt": {
    "server": "mqtt.example.com",
    "topics": ["msh/region/#"]
  },
  "cleanup": {
    "enabled": "false",
    "days_to_keep": "14",
    "hour": "2",
    "minute": "0",
    "vacuum": "false"
  }
}
```

---

## 7. Language API

### GET `/api/lang`
Returns translation strings.

Query Parameters
- `lang` (optional, string): Language code (e.g., `en`, `es`). Default from config or `en`.
- `section` (optional, string): Return only one section (e.g., `nodelist`, `firehose`).

Response Example
```json
{
  "title": "Meshview",
  "search_placeholder": "Search..."
}
```

---

## 8. Packets Seen API

### GET `/api/packets_seen/{packet_id}`
Returns packet_seen entries for a packet.

Path Parameters
- `packet_id` (required, int): Packet ID.

Response Example
```json
{
  "seen": [
    {
      "packet_id": 123,
      "node_id": 456,
      "rx_time": "2025-07-22T12:45:00",
      "hop_limit": 7,
      "hop_start": 0,
      "channel": "main",
      "rx_snr": 5.0,
      "rx_rssi": -90,
      "topic": "msh/region/#",
      "import_time_us": 1736370123456789
    }
  ]
}
```

---

## 9. Traceroute API

### GET `/api/traceroute/{packet_id}`
Returns traceroute details and derived paths for a packet.

Path Parameters
- `packet_id` (required, int): Packet ID.

Response Example
```json
{
  "packet": {
    "id": 123,
    "from": 111,
    "to": 222,
    "channel": "main"
  },
  "traceroute_packets": [
    {
      "index": 0,
      "gateway_node_id": 333,
      "done": true,
      "forward_hops": [111, 444, 222],
      "reverse_hops": [222, 444, 111]
    }
  ],
  "unique_forward_paths": [
    { "path": [111, 444, 222], "count": 2 }
  ],
  "unique_reverse_paths": [
    [222, 444, 111]
  ],
  "winning_paths": [
    [111, 444, 222]
  ]
}
```

---

## 10. Health API

### GET `/health`
Returns service health and database status.

Response Example
```json
{
  "status": "healthy",
  "timestamp": "2025-07-22T12:45:00+00:00",
  "version": "3.0.3",
  "git_revision": "abc1234",
  "database": "connected",
  "database_size": "12.34 MB",
  "database_size_bytes": 12939444
}
```

---

## 11. Version API

### GET `/version`
Returns version metadata.

Response Example
```json
{
  "version": "3.0.3",
  "release_date": "2026-1-15",
  "git_revision": "abc1234",
  "git_revision_short": "abc1234"
}
```
