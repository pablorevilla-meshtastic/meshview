
# API Documentation

## 1. Chat API

### GET `/api/chat`
Returns the most recent chat messages.

**Query Parameters**
- `limit` (optional, int): Maximum number of messages to return. Default: `100`.

**Response Example**
```json
{
  "packets": [
    {
      "id": 123,
      "import_time": "2025-07-22T12:45:00",
      "from_node_id": 987654,
      "from_node": "Alice",
      "channel": "main",
      "payload": "Hello, world!"
    }
  ]
}
```

---

### GET `/api/chat/updates`
Returns chat messages imported after a given timestamp.

**Query Parameters**
- `last_time` (optional, ISO timestamp): Only messages imported after this time are returned.

**Response Example**
```json
{
  "packets": [
    {
      "id": 124,
      "import_time": "2025-07-22T12:50:00",
      "from_node_id": 987654,
      "from_node": "Alice",
      "channel": "main",
      "payload": "New message!"
    }
  ],
  "latest_import_time": "2025-07-22T12:50:00"
}
```

---

## 2. Nodes API

### GET `/api/nodes`
Returns a list of all nodes, with optional filtering by last seen.

**Query Parameters**
- `hours` (optional, int): Return nodes seen in the last N hours.
- `days` (optional, int): Return nodes seen in the last N days.
- `last_seen_after` (optional, ISO timestamp): Return nodes seen after this time.

**Response Example**
```json
{
  "nodes": [
    {
      "node_id": 1234,
      "long_name": "Alice",
      "short_name": "A",
      "channel": "main",
      "last_seen": "2025-07-22T12:40:00",
      "hardware": "T-Beam",
      "firmware": "1.2.3",
      "role": "client",
      "last_lat": 37.7749,
      "last_long": -122.4194
    }
  ]
}
```

---

## 3. Packets API

### GET `/api/packets`
Returns a list of packets with optional filters.

**Query Parameters**
- `limit` (optional, int): Maximum number of packets to return. Default: `200`.
- `since` (optional, ISO timestamp): Only packets imported after this timestamp are returned.

**Response Example**
```json
{
  "packets": [
    {
      "id": 123,
      "from_node_id": 5678,
      "to_node_id": 91011,
      "portnum": 1,
      "import_time": "2025-07-22T12:45:00",
      "payload": "Hello, Bob!"
    }
  ]
}
```

---

---

## 4. Channels API

### GET `/api/channels`
Returns a list of channels seen in a given time period.

**Query Parameters**
- `period_type` (optional, string): Time granularity (`hour` or `day`). Default: `hour`.
- `length` (optional, int): Number of periods to look back. Default: `24`.

**Response Example**
```json
{
  "channels": ["LongFast", "MediumFast", "ShortFast"]
}
```

---

## 5. Statistics API

### GET `/api/stats`

Retrieve packet statistics aggregated by time periods, with optional filtering.

---

## Query Parameters

| Parameter    | Type    | Required | Default  | Description                                                                                       |
|--------------|---------|----------|----------|-------------------------------------------------------------------------------------------------|
| `period_type` | string  | No       | `hour`   | Time granularity of the stats. Allowed values: `hour`, `day`.                                   |
| `length`      | integer | No       | 24       | Number of periods to include (hours or days).                                                   |
| `channel`     | string  | No       | —        | Filter results by channel name (case-insensitive).                                             |
| `portnum`     | integer | No       | —        | Filter results by port number.                                                                  |
| `to_node`     | integer | No       | —        | Filter results to packets sent **to** this node ID.                                            |
| `from_node`   | integer | No       | —        | Filter results to packets sent **from** this node ID.                                          |

---

## Response

```json
{
  "period_type": "hour",
  "length": 24,
  "channel": "LongFast",
  "portnum": 1,
  "to_node": 12345678,
  "from_node": 87654321,
  "data": [
    {
      "period": "2025-08-08 14:00",
      "count": 10
    },
    {
      "period": "2025-08-08 15:00",
      "count": 7
    }
    // more entries...
  ]
}
```

---

## 6. Edges API

### GET `/api/edges`
Returns network edges (connections between nodes) based on traceroutes and neighbor info.

**Query Parameters**
- `type` (optional, string): Filter by edge type (`traceroute` or `neighbor`). If omitted, returns both types.

**Response Example**
```json
{
  "edges": [
    {
      "from": 12345678,
      "to": 87654321,
      "type": "traceroute"
    },
    {
      "from": 11111111,
      "to": 22222222,
      "type": "neighbor"
    }
  ]
}
```

---

## 7. Configuration API

### GET `/api/config`
Returns the current site configuration (safe subset exposed to clients).

**Response Example**
```json
{
  "site": {
    "domain": "meshview.example.com",
    "language": "en",
    "title": "Bay Area Mesh",
    "message": "Real time data from around the bay area",
    "starting": "/chat",
    "nodes": "true",
    "conversations": "true",
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
    "version": "2.0.8 ~ 10-22-25"
  },
  "mqtt": {
    "server": "mqtt.bayme.sh",
    "topics": ["msh/US/bayarea/#"]
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

## 8. Language/Translations API

### GET `/api/lang`
Returns translation strings for the UI.

**Query Parameters**
- `lang` (optional, string): Language code (e.g., `en`, `es`). Defaults to site language setting.
- `section` (optional, string): Specific section to retrieve translations for.

**Response Example (full)**
```json
{
  "chat": {
    "title": "Chat",
    "send": "Send"
  },
  "map": {
    "title": "Map",
    "zoom_in": "Zoom In"
  }
}
```

**Response Example (section-specific)**
Request: `/api/lang?section=chat`
```json
{
  "title": "Chat",
  "send": "Send"
}
```

---

## 9. Health Check API

### GET `/health`
Health check endpoint for monitoring, load balancers, and orchestration systems.

**Response Example (Healthy)**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T14:30:00.123456Z",
  "version": "3.0.0",
  "git_revision": "6416978",
  "database": "connected",
  "database_size": "853.03 MB",
  "database_size_bytes": 894468096
}
```

**Response Example (Unhealthy)**
Status Code: `503 Service Unavailable`
```json
{
  "status": "unhealthy",
  "timestamp": "2025-11-03T14:30:00.123456Z",
  "version": "2.0.8",
  "git_revision": "6416978",
  "database": "disconnected"
}
```

---

## 10. Version API

### GET `/version`
Returns detailed version information including semver, release date, and git revision.

**Response Example**
```json
{
  "version": "2.0.8",
  "release_date": "2025-10-22",
  "git_revision": "6416978a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q",
  "git_revision_short": "6416978"
}
```

---

## Notes
- All timestamps (`import_time`, `last_seen`) are returned in ISO 8601 format.
- `portnum` is an integer representing the packet type.
- `payload` is always a UTF-8 decoded string.
- Node IDs are integers (e.g., `12345678`).
