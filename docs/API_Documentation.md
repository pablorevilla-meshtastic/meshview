# API Documentation

Base URL: `http(s)://<host>`

This reference covers all 16 GET routes registered in `meshview/web_api/api.py`,
including `/health` and `/version`. The browser version is served at `/api.html`.
Responses below are illustrative examples; actual values depend on stored data.
Regenerate the browser reference after editing this file with
`node scripts/build-api-docs.mjs`.

## Conventions

- Successful API responses are JSON. Explicit validation errors usually return JSON
  with an `error` field. Some unhandled errors return HTTP 500 with a plain-text
  body; check HTTP status and Content-Type before parsing an error response.
- All routes are read-only. The application does not require an API token; a reverse
  proxy may impose authentication. There are no application-level write endpoints.
- `*_us` timestamps and `since` use microseconds since the Unix epoch. Snapshot dates
  and statistics buckets use UTC. Node latitude/longitude integers must be divided
  by 10,000,000 to obtain degrees; coverage coordinates are already degrees.
- Packet `id` and `storage_id` are database row IDs. Use these for the `packet_id`
  query/path parameters on packet, observation, count, and traceroute endpoints.
  A response field named `packet_id` on a packet object is instead its over-the-air
  Meshtastic ID. `reply_id`, when present, is also an over-the-air ID. These ID types
  are not interchangeable. Node IDs are numeric Meshtastic node numbers; the node
  object's `id` is a separate string identifier.
- Use decimal node IDs throughout. The packet sender/recipient filters and the QR
  and coverage paths also accept Python-style `0x` hexadecimal numbers. This is
  not supported consistently by the other routes.
- Public broadcast text is readable. Direct text messages on port 1 are returned as
  `<redacted>`. Request chat with `/api/packets?portnum=1`; there is no `/api/chat`
  route. Do not treat a decoded `payload` string as trusted HTML.

## Quick examples

```sh
curl 'http://localhost:8081/api/nodes?days_active=3'
curl 'http://localhost:8081/api/packets?portnum=1&limit=100'
curl 'http://localhost:8081/api/stats/count'
curl 'http://localhost:8081/api/coverage/1234?mode=perimeter&radius_km=20'
```

## 1. Nodes API

### GET `/api/nodes`
Returns a list of nodes, with optional filtering.

Query Parameters
- `node_id` (optional, int): Exact node ID.
- `role` (optional, string): Node role.
- `channel` (optional, string): Channel name.
- `hw_model` (optional, string): Hardware model.
- `days_active` (optional, int): Nodes seen within the last N days. Omit for all
  nodes with a non-null last-seen timestamp; invalid integers are ignored.

Nodes are sorted by `short_name` ascending. `role` is normalized to uppercase;
channel and hardware filters are exact matches. No pagination is implemented.

Errors: HTTP 500 with `{"error":"Failed to fetch nodes"}` for handler failures;
the storage helper may return an empty list for database failures.

Response Example
```json
{
  "nodes": [
    {
      "id": "!000004d2",
      "node_id": 1234,
      "long_name": "Alice",
      "short_name": "A",
      "hw_model": "T-Beam",
      "firmware": "1.2.3",
      "role": "client",
      "last_lat": 377749000,
      "last_long": -1224194000,
      "last_altitude": 125,
      "channel": "main",
      "is_mqtt_gateway": true,
      "first_seen_us": 1736283723456789,
      "last_seen_us": 1736370123456789
    }
  ]
}
```

`last_altitude` is the latest reported altitude in meters above sea level, or `null`
when unknown. It updates with valid node locations from position packets and map reports.
Position packets without altitude preserve the previous value. Map reports lack altitude
field presence, so zero values in map reports also preserve the previous value.
Existing nodes receive altitude as new reports arrive.

---

## 2. Packets API

### GET `/api/packets`
Returns packets with optional filters.

Query Parameters
- `packet_id` (optional, decimal int): Return one packet by database row ID (overrides other filters).
- `limit` (optional, int): Max packets to return, clamped 1-1000. Default: `50`.
- `since` (optional, int): Only packets imported after this microsecond timestamp.
- `portnum` (optional, int): Filter by port number.
- `contains` (optional, string): Payload substring filter.
- `from_node_id` (optional, int): Filter by sender node ID.
- `channel` (optional, string): Filter by exact channel name before applying the packet limit.
- `to_node_id` (optional, int): Filter by recipient node ID.
- `node_id` (optional, int): Legacy filter matching either from or to node ID.

Response Example
```json
{
  "packets": [
    {
      "id": 123,
      "storage_id": 123,
      "packet_id": 3314808102,
      "import_time_us": 1736370123456789,
      "channel": "main",
      "from_node_id": 5678,
      "to_node_id": 4294967295,
      "portnum": 1,
      "long_name": "Alice",
      "payload": "Hello, mesh!",
      "to_long_name": null,
      "reply_id": 122
    }
  ],
  "latest_import_time": 1736370123456789
}
```

Notes
- For `portnum=1` (text messages), packets are filtered to remove sequence-only payloads.
- Results are newest first. `since` is strictly greater than the supplied timestamp.
  Store `latest_import_time` for the next poll and deduplicate by `id`. A bounded
  result can omit older records if more packets arrive than the requested limit;
  this endpoint is not a durable cursor or backfill API.
- `latest_import_time` is returned only when the list response has a positive import
  timestamp; it is absent for empty results and single-packet lookups.
- `packet_id` lookup returns `{"packets":[]}` with HTTP 200 when missing. Its objects
  omit `to_long_name` and `reply_id`; nullable `portnum` is possible in this mode.
- `contains` is case-insensitive. With `portnum=1`, matching is performed on decoded
  displayed payload text (including redaction placeholders) after the database limit is applied, so fewer than `limit` results
  may be returned. For other requests, it searches stored payload bytes cast to text;
  this is not a general search over decoded protobuf fields.
- Invalid `limit` falls back to 50. Invalid `since`, `portnum`, and node filters are
  logged and ignored. Invalid single-packet IDs return HTTP 400; handler failures
  return HTTP 500 with `{"error":"Failed to fetch packets"}`.

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

Errors: storage/period failures return HTTP 200 with `channels: []` and an `error`
field. Non-integer `length` is parsed outside that handler and can return HTTP 500.
Use a positive integer length and the literal `hour` or `day`.

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
  "sent": 0,
  "seen": 0
}
```

---

The series response contains only buckets with records, ordered oldest first;
missing hours/days are not filled with zeroes. Periods are UTC strings.

Current `node`-mode limitation: the handler reads a `total` key that the statistics
helper does not provide, so `sent` and `seen` currently return zero. It also uses
recipient filtering for the second query, rather than gateway observations. This
mode ignores the other filters. For usable sent/observation totals, request
`/api/stats/count?from_node=1234&period_type=day&length=1` instead.

Errors: HTTP 400 for an unsupported `period_type`, non-integer `length`, `node`,
`portnum`, `from_node`, or `to_node`. Storage failures can return HTTP 500.
Use a positive `length`; the handler does not impose a positive lower bound.

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

Without filters, counts cover the whole retained database. With time, channel,
or direction filters, omitted time settings default to `period_type=day&length=1`.
`total_seen` counts observation rows for packets matching the packet import-time
window, not distinct gateways. Channel matching is case-insensitive.

`packet_id` applies only to `total_seen` and overrides its other filters: it counts
all observations of that database packet ID. It does not narrow `total_packets`.
In particular, `packet_id` alone leaves `total_packets` as the global packet total.

Errors: HTTP 400 for non-integer ID/length filters. Unsupported `period_type` or
storage failures can return HTTP 500; use `hour` or `day` and a positive length.

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

`sent` counts packet records from each node; `seen` counts observation records for
that sender's packets. `avg` is `round(seen / max(sent, 1), 2)`, not a distinct-gateway
count. Windows are anchored to the newest packet and newest observation in the
respective tables, not wall-clock time. Nodes with zero activity are included;
`total` counts nodes matching the channel filter, not just active nodes.

Channel matching is exact. Use positive `length` and `limit`, and a nonnegative
`offset`. Only the upper limit of 100 is enforced. Invalid numeric strings can
return HTTP 500; any `period_type` other than the literal `hour` is treated as days.

## 5. Edges API

### GET `/api/edges`
Returns network edges (connections between nodes) based on traceroutes and neighbor info.
Traceroute edges are collected over the last 12 hours. Neighbor edges are based on
port 71 packets.

A completed traceroute is observed as a response packet, whose `from`/`to` are reversed
with respect to the traced path, so edges are built as `to -> route[] -> from`. `route[]`
may contain `0xFFFFFFFF` placeholders for hops the mesh could not identify; the edges on
either side of such a placeholder are omitted, because the nodes around an unknown hop
are not neighbours.

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

Unknown `type` values return an empty edge list. Invalid `node_id` returns HTTP 400;
storage failures can return HTTP 500. A missing node is not an error and normally
returns an empty list. Neighbor edges come from the latest stored port-71 sample
(the storage helper defaults to 50 packets), not the traceroute 12-hour window.

## 6. Daily Snapshots and Configuration

### GET `/api/snapshots/daily`

Returns stored daily snapshots. For new snapshots, `packet_count` is the number of
packet records imported during `date` (00:00 UTC inclusive to the next midnight
exclusive). The scheduled capture records the previous complete UTC day. Repeated
observations of the same packet are not counted separately. `node_count` counts distinct
packet senders whose packets were imported or observed during that UTC day (including
observations of previously imported packets). `gateway_count` counts distinct MQTT
gateways with packet observations imported during that day. These are activity counts,
not database totals; recipients alone do not count as active nodes. Activity uses local
import timestamps, not device timestamps. Older snapshots retain their originally stored
counts and are not automatically converted. Counts depend on the packet and observation
history still retained at capture time.

Query Parameters

- `length` (optional, int): Return the latest N snapshot records, clamped to 1-3650.
  Omit for all stored snapshots. Results are always ordered by date ascending.
  This is a record limit, not a guarantee of consecutive calendar dates.

Response Example

```json
{"data":[{"date":"2026-10-24","node_count":143,"packet_count":28465,"gateway_count":17,"captured_at_us":1792886400000000}]}
```

No stored snapshots returns `{"data":[]}`. Invalid `length` returns HTTP 400;
storage failures return HTTP 500. `captured_at_us` is the capture time, which may
be later than the day summarized by `date`.

### GET `/api/config`
Returns a safe subset of server configuration.

`site.map_channel_colors` contains channel color overrides from the optional
`[map_channel_colors]` INI section. Each entry is `channel = #RRGGBB`; invalid colors
are omitted. Channel matching on the map ignores case, spaces, hyphens, and underscores.
Unlisted channels use generated colors. For example:

```ini
[map_channel_colors]
LongFast = #4363d8
LocalChat = #18aa18
```

No query parameters are supported. Only the `site`, MQTT server/topics, and cleanup
fields shown here are exposed; credentials and the database connection string are
not returned. Feature flags and cleanup booleans are lowercase strings (`"true"` /
`"false"`), not JSON booleans. Cleanup scheduling values are strings; map bounds are
numbers and refresh intervals are integers. The removed `starting` option is not
returned: `/` always serves the dashboard. `site.api` controls visibility of the API
documentation link in the navigation bar, defaults to `"true"`, and can be disabled
with `api = False` in `[site]`. This setting does not disable documentation or API
routes. Restart the web server and reload the page after changing it. Handler
failures return HTTP 500.

Restart the web server and reload the map after changing these settings. Omitting
the section uses generated colors for every channel.

Response Example
```json
{
  "site": {
    "domain": "example.com",
    "language": "en",
    "title": "Meshview",
    "message": "",
    "nodes": "true",
    "chat": "true",
    "everything": "true",
    "graphs": "true",
    "stats": "true",
    "net": "true",
    "map": "true",
    "top": "true",
    "api": "true",
    "map_top_left_lat": 39.0,
    "map_top_left_lon": -123.0,
    "map_bottom_right_lat": 36.0,
    "map_bottom_right_lon": -121.0,
    "map_interval": 3,
    "map_channel_colors": {"LongFast":"#4363d8"},
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

Unknown or invalid language codes fall back to the English file. An unknown section
returns HTTP 404. The response has no wrapper: it is either the full translation
object or the requested section. Translation-file failures can return HTTP 500.

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
      "rx_time": 1753188300,
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

`node_id` identifies the observing MQTT gateway. `rx_time` is the device-provided
receive time in Unix seconds, while `import_time_us` is local import time
in microseconds. Signal fields can be null. Multiple rows can describe the same
gateway; consumers wanting unique gateways must deduplicate them. Hop count is
usually `max(0, hop_start - hop_limit)` when both values are known. Observations
do not by themselves prove a direct radio link from the sender to that gateway.

No observations, including for an unknown packet, returns `{"seen":[]}` with HTTP
200. Invalid path IDs return HTTP 400; handler failures return HTTP 500.

## 9. Traceroute API

### GET `/api/traceroute/{packet_id}`
Returns traceroute details and derived paths for a packet.

Path Parameters
- `packet_id` (required, int): Packet ID.

A completed traceroute is observed as a response packet, whose `from`/`to` are reversed
with respect to the traced path. `initiator` and `target` resolve this: the forward path
runs `initiator -> forward_hops -> target` and the return path runs
`target -> reverse_hops -> initiator`, in both directions of travel. `forward_hops` and
`reverse_hops` contain only the intermediate hops, never the endpoints.

A gateway usually reports a response that is still travelling home, so `reverse_hops` is
often incomplete. `reverse_complete` says whether that observation had reached the
initiator; only then does the corresponding `winning_paths.reverse` entry end at the
initiator.

`winning_paths` is built from response observations, since a response proves the request
reached the target. `complete` on a `unique_forward_paths` entry says whether some
response reported that hop list, and so whether it is known to end at the target.

Response Example
```json
{
  "packet": {
    "id": 123,
    "from": 222,
    "to": 111,
    "initiator": 111,
    "target": 222,
    "channel": "main"
  },
  "traceroute_packets": [
    {
      "index": 0,
      "gateway_node_id": 333,
      "done": true,
      "forward_hops": [444, 555],
      "reverse_hops": [555, 444],
      "reverse_complete": true
    }
  ],
  "unique_forward_paths": [
    { "path": [444, 555], "count": 2, "complete": true }
  ],
  "unique_reverse_paths": [
    [555, 444]
  ],
  "winning_paths": {
    "forward": [[111, 444, 555, 222]],
    "reverse": [[222, 555, 444, 111]]
  }
}
```

---

`traceroute_packets` can be empty even when the packet exists. Unknown database
packet IDs return HTTP 404. Invalid integer IDs and storage failures can return
HTTP 500; this handler does not implement a separate HTTP 400 validation branch.

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
  "cleanup": {
    "enabled": true,
    "days_to_keep": 14,
    "scheduled_time": "02:00",
    "vacuum": false,
    "status": "ok",
    "status_file": "dbcleanup.status.json",
    "last_run": {
      "status": "ok",
      "started_at": "2026-06-04T09:00:00+00:00",
      "completed_at": "2026-06-04T09:00:03+00:00",
      "cutoff_at": "2026-05-21T09:00:00+00:00",
      "days_to_keep": 14,
      "vacuum_requested": false,
      "vacuum_completed": false,
      "rows_deleted": {
        "packet": 1200,
        "packet_seen": 3400,
        "traceroute": 42,
        "node": 3
      },
      "error": null
    }
  },
  "backup": {
    "enabled": true,
    "backup_dir": "./backups",
    "scheduled_time": "02:00",
    "status": "ok",
    "status_file": "dbbackup.status.json",
    "last_run": {
      "status": "ok",
      "started_at": "2026-06-04T09:00:00+00:00",
      "completed_at": "2026-06-04T09:00:02+00:00",
      "backup_dir": "./backups",
      "database_path": "packets.db",
      "backup_file": "backups/packets_backup_20260604_090000.db.gz",
      "original_size_bytes": 12939444,
      "compressed_size_bytes": 4211560,
      "compression_percent": 67.5,
      "error": null
    }
  },
  "database": "connected",
  "database_size": "12.34 MB",
  "database_size_bytes": 12939444
}
```

---

No query parameters. HTTP 200 reports `status: "healthy"` with database connectivity.
A database failure returns HTTP 503 with `status: "unhealthy"` and
`database: "disconnected"`. `seconds_since_last_message` is included only when a
latest imported packet exists; SQLite size fields appear only when available.
Cleanup and backup reports include configured schedules and status-file contents
when present. Their status may be `disabled`, `unknown`, `error`, or the last job's
recorded status; a failed backup/cleanup does not itself change the top-level HTTP
status. The optional `last_run` objects depend on the job's stored report.

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

No query parameters. HTTP 500 with an `error` field if version metadata cannot be
retrieved. A revision may be `unknown` if Git metadata is unavailable.

## 12. Node Contact URL

### GET `/api/node/{node_id}/qr`

Returns a Meshtastic shared-contact URL as JSON, not a PNG or SVG image. The client
can encode `meshtastic_url` in a QR code. No query parameters are supported.

Path Parameters

- `node_id` (required, int): Node number in decimal or `0x` hexadecimal form.

Response Example

```json
{
  "node_id":1234,
  "long_name":"Alice",
  "short_name":"A",
  "role":"CLIENT",
  "meshtastic_url":"https://meshtastic.org/v/#BASE64URL_CONTACT"
}
```

The example contact payload is a placeholder, not an importable contact. The URL
encodes node identity and available user metadata as a base64url SharedContact
protobuf, with `manually_verified` false. Metadata can be null.

Errors: HTTP 400 for invalid IDs; HTTP 404 when the node is absent; HTTP 500 for
contact serialization failures or unhandled storage errors.

## 13. Predicted Radio Coverage

### GET `/api/coverage/{node_id}`

Computes an ITM area-model prediction centered on the node's last stored position.
This is a model prediction, not a measured coverage boundary or terrain profile.
The optional `pyitm` dependency is required. Calculations run off the event loop
and reuse cached model results. All parameters are optional except the node ID.

Path Parameters

- `node_id` (required, int): Node number in decimal or `0x` hexadecimal form.

Query Parameters

- `mode` (string, default `perimeter`): `perimeter` or `heatmap`. Currently every
  value other than the exact string `perimeter` selects the heatmap branch.
- `freq_mhz` (number, default `907`): Frequency in MHz; range 1-10000.
- `tx_dbm` (number, default `20`): Transmit power in dBm; range -50 to 60.
- `tx_height_m` (number, default `5`): Transmit antenna height in meters; range 0-1000.
- `rx_height_m` (number, default `1.5`): Receive antenna height in meters; range 0-1000.
- `radius_km` (number, default `40`): Maximum distance in kilometers; range 1-200.
- `step_km` (number, default `0.25`): Radial sample spacing in kilometers; range 0.05-50.
- `reliability` (number, default `0.5`): ITM time fraction; range 0.01-0.99.
- `threshold_dbm` (number, default `-120`): Perimeter received-power threshold in dBm;
  range -200 to 0. Ignored by heatmap computation, although still validated.

Numeric bounds are inclusive, values must be finite, and `radius_km / step_km`
must not exceed 4000. Smaller steps increase computation cost.

Response Example (`mode=perimeter`)

```json
{
  "mode":"perimeter",
  "threshold_dbm":-120.0,
  "perimeter":[[30.21,-93.20],[30.209,-93.198]]
}
```

`perimeter` contains `[latitude, longitude]` degree pairs for the furthest qualifying
sample on each modeled bearing. Bearings with no qualifying sample are omitted;
the list is not necessarily a closed GeoJSON polygon.

Response Example (`mode=heatmap`)

```json
{
  "mode":"heatmap",
  "min_dbm":-130.0,
  "max_dbm":-80.0,
  "points":[[30.21,-93.20,-110.5]]
}
```

`points` contains `[latitude, longitude, received_power_dbm]` triples. Min/max values
provide a color-scale range, extended from the defaults to include computed values.
An empty perimeter or point list is a valid result when no samples qualify.

Errors: HTTP 400 for invalid IDs, nonnumeric/nonfinite/out-of-range parameters, or
an excessive radius/step ratio; HTTP 404 for an unknown node or missing/zero-valued
stored coordinates; HTTP 503 when `pyitm` is unavailable. Dependency availability is checked
before numeric query validation and node lookup. Unexpected model/storage failures
can return HTTP 500.
