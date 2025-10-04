# Database Portability Implementation

## Summary

Meshview now supports both SQLite and PostgreSQL databases through a database-agnostic implementation. The database type is automatically detected from the connection string in `config.ini`.

## Why PostgreSQL and Not MySQL?

PostgreSQL was chosen as the production database option over MySQL for several technical reasons:

1. **Native ON CONFLICT Support** - PostgreSQL has native `ON CONFLICT DO NOTHING` syntax (similar to SQLite), making the code migration cleaner
2. **Better Concurrent Operations** - PostgreSQL handles concurrent reads/writes better, which is critical for Meshview's two-process architecture (separate database ingestion and web serving processes)
3. **Superior Time-Series Performance** - Meshview stores heavily time-based packet data; PostgreSQL excels at time-series workloads
4. **Async Driver Maturity** - The `asyncpg` driver is highly optimized and battle-tested for async Python applications
5. **JSON Support** - Better native JSON handling if future features need to query protobuf payloads directly

While MySQL would work with the database-agnostic implementation, PostgreSQL provides better performance characteristics for Meshview's specific use case.

## Changes Made

### 1. Database Module Updates

**File: `meshview/database.py`**
- Added database type detection based on connection string
- SQLite-specific settings (read-only mode, URI mode) now only apply to SQLite
- PostgreSQL can now connect without SQLite-specific parameters

**File: `meshview/mqtt_database.py`**
- Added database type detection based on connection string
- SQLite timeout parameter now only applies to SQLite databases
- PostgreSQL uses default connection settings

### 2. Database-Agnostic INSERT Operations

**File: `meshview/mqtt_store.py`**
- Removed SQLite-specific `insert().on_conflict_do_nothing()` syntax
- Implemented try/except with `IntegrityError` for duplicate key handling
- This approach works identically for SQLite, PostgreSQL, and other databases

**Before:**
```python
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
stmt = sqlite_insert(Packet).values(...).on_conflict_do_nothing()
```

**After:**
```python
from sqlalchemy.exc import IntegrityError
try:
    packet = Packet(...)
    session.add(packet)
    await session.flush()
except IntegrityError:
    await session.rollback()  # Duplicate key, skip
```

### 3. Configuration Documentation

**Files Updated:**
- `sample.config.ini` - Added PostgreSQL connection string examples
- `README.md` - Added PostgreSQL connection string examples

## Using PostgreSQL

### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

### 2. Create Database

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE meshview;
CREATE USER meshview_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE meshview TO meshview_user;
\q
```

### 3. Update config.ini

```ini
[database]
connection_string = postgresql+asyncpg://meshview_user:your_password@localhost/meshview
```

### 4. Run Meshview

The application will automatically:
- Detect it's connecting to PostgreSQL
- Create all necessary tables on first run
- Use database-agnostic operations

## Benefits

### SQLite (Default)
- ✅ Single file database
- ✅ No separate server needed
- ✅ Easy backup (copy the file)
- ✅ Perfect for small to medium deployments

### PostgreSQL (Production)
- ✅ Better concurrent read/write performance
- ✅ Superior for high-throughput deployments
- ✅ Better handling of time-series data
- ✅ Native support for concurrent operations
- ✅ Better for multiple node ingestion

## Migration from SQLite to PostgreSQL

If you want to migrate existing SQLite data to PostgreSQL:

1. **Create PostgreSQL database** (see above)

2. **Update config.ini** with PostgreSQL connection string

3. **Run startdb.py** to create tables:
   ```bash
   ./env/bin/python startdb.py
   ```

4. **Optional: Import existing data**
   - You can use SQLAlchemy to read from SQLite and write to PostgreSQL
   - Or export/import specific data as needed

## Testing

The implementation has been tested to ensure:
- SQLite continues to work as before (backward compatible)
- PostgreSQL connections work correctly
- All database operations are truly database-agnostic
- No performance degradation

## Technical Details

### Database Type Detection
```python
if 'sqlite' in database_connection_string.lower():
    # Apply SQLite-specific settings
```

### IntegrityError Handling
The `IntegrityError` exception is part of SQLAlchemy's core and is raised consistently across all database backends when a unique constraint is violated.

## Questions?

For issues or questions about database configuration, please refer to:
- SQLAlchemy documentation: https://docs.sqlalchemy.org/
- PostgreSQL documentation: https://www.postgresql.org/docs/
