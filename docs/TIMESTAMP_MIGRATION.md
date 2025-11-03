# High-Resolution Timestamp Migration

This document describes the implementation of GitHub issue #55: storing high-resolution timestamps as integers in the database for improved performance and query efficiency.

## Overview

The meshview database now stores timestamps in two formats:
1. **TEXT format** (`import_time`): Human-readable ISO8601 format with microseconds (e.g., `2025-03-12 04:15:56.058038`)
2. **INTEGER format** (`import_time_us`): Microseconds since Unix epoch (1970-01-01 00:00:00 UTC)

The dual format approach provides:
- **Backward compatibility**: Existing `import_time` TEXT columns remain unchanged
- **Performance**: Fast integer comparisons and math operations
- **Precision**: Microsecond resolution for accurate timing
- **Efficiency**: Compact storage and fast indexed lookups

## Database Changes

### New Columns Added

Three tables have new `import_time_us` columns:

1. **packet.import_time_us** (INTEGER)
   - Stores when the packet was imported into the database
   - Indexed for fast queries

2. **packet_seen.import_time_us** (INTEGER)
   - Stores when the packet_seen record was imported
   - Indexed for performance

3. **traceroute.import_time_us** (INTEGER)
   - Stores when the traceroute was imported
   - Indexed for fast lookups

### New Indexes

The following indexes were created for optimal query performance:

```sql
CREATE INDEX idx_packet_import_time_us ON packet(import_time_us DESC);
CREATE INDEX idx_packet_from_node_time_us ON packet(from_node_id, import_time_us DESC);
CREATE INDEX idx_packet_seen_import_time_us ON packet_seen(import_time_us);
CREATE INDEX idx_traceroute_import_time_us ON traceroute(import_time_us);
```

## Migration Process

### For Existing Databases

Run the migration script to add the new columns and populate them from existing data:

```bash
python migrate_add_timestamp_us.py [database_path]
```

If no path is provided, it defaults to `packets.db` in the current directory.

The migration script:
1. Checks if migration is needed (idempotent)
2. Adds `import_time_us` columns to the three tables
3. Populates the new columns from existing `import_time` values
4. Creates indexes for optimal performance
5. Verifies the migration completed successfully

### For New Databases

New databases created with the updated schema will automatically include the `import_time_us` columns. The MQTT store module populates both columns when inserting new records.

## Code Changes

### Models (meshview/models.py)

The ORM models now include the new `import_time_us` fields:

```python
class Packet(Base):
    import_time: Mapped[datetime] = mapped_column(nullable=True)
    import_time_us: Mapped[int] = mapped_column(BigInteger, nullable=True)
```

### MQTT Store (meshview/mqtt_store.py)

The data ingestion logic now populates both timestamp columns using UTC time:

```python
now = datetime.datetime.now(datetime.timezone.utc)
now_us = int(now.timestamp() * 1_000_000)

# Both columns are populated
import_time=now,
import_time_us=now_us,
```

**Important**: All new timestamps use UTC (Coordinated Universal Time) for consistency across time zones.

## Using the New Timestamps

### Example Queries

**Query packets from the last 7 days:**

```sql
-- Old way (slower)
SELECT * FROM packet 
WHERE import_time >= datetime('now', '-7 days');

-- New way (faster)
SELECT * FROM packet
WHERE import_time_us >= (strftime('%s', 'now', '-7 days') * 1000000);
```

**Query packets in a specific time range:**

```sql
SELECT * FROM packet
WHERE import_time_us BETWEEN 1759254380000000 AND 1759254390000000;
```

**Calculate time differences (in microseconds):**

```sql
SELECT 
    id,
    (import_time_us - LAG(import_time_us) OVER (ORDER BY import_time_us)) / 1000000.0 as seconds_since_last
FROM packet
LIMIT 10;
```

### Converting Timestamps

**From datetime to microseconds (UTC):**
```python
import datetime
now = datetime.datetime.now(datetime.timezone.utc)
now_us = int(now.timestamp() * 1_000_000)
```

**From microseconds to datetime:**
```python
import datetime
timestamp_us = 1759254380813451
dt = datetime.datetime.fromtimestamp(timestamp_us / 1_000_000)
```

**In SQL queries:**
```sql
-- Datetime to microseconds
SELECT CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER);

-- Microseconds to datetime (approximate)
SELECT datetime(import_time_us / 1000000, 'unixepoch');
```

## Performance Benefits

The integer timestamp columns provide significant performance improvements:

1. **Faster comparisons**: Integer comparisons are much faster than string/datetime comparisons
2. **Smaller index size**: Integer indexes are more compact than datetime indexes
3. **Range queries**: BETWEEN operations on integers are highly optimized
4. **Math operations**: Easy to calculate time differences, averages, etc.
5. **Sorting**: Integer sorting is faster than datetime sorting

## Backward Compatibility

The original `import_time` TEXT columns remain unchanged:
- Existing code continues to work
- Human-readable timestamps still available
- Gradual migration to new columns possible
- No breaking changes for existing queries

## Future Work

Future improvements could include:
- Migrating queries to use `import_time_us` columns
- Deprecating the TEXT `import_time` columns (after transition period)
- Adding helper functions for timestamp conversion
- Creating views that expose both formats

## Testing

The migration was tested on a production database with:
- 132,466 packet records
- 1,385,659 packet_seen records  
- 28,414 traceroute records

All records were successfully migrated with microsecond precision preserved.

## References

- GitHub Issue: #55 - Storing High-Resolution Timestamps in SQLite
- SQLite datetime functions: https://www.sqlite.org/lang_datefunc.html
- Python datetime module: https://docs.python.org/3/library/datetime.html
