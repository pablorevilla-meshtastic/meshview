
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

### Notes
- All timestamps (`import_time`, `last_seen`) are returned in ISO 8601 format.
- `portnum` is an integer representing the packet type.
- `payload` is always a UTF-8 decoded string.

## 4 Statistics API: GET `/api/stats`

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
