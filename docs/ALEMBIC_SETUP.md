# Alembic Database Migration Setup

This document describes the automatic database migration system implemented for MeshView using Alembic.

## Overview

The system provides automatic database schema migrations with coordination between the writer app (startdb.py) and reader app (web.py):

- **Writer App**: Automatically runs pending migrations on startup
- **Reader App**: Waits for migrations to complete before starting

## Architecture

### Key Components

1. **`meshview/migrations.py`** - Migration management utilities
   - `run_migrations()` - Runs pending migrations (writer app)
   - `wait_for_migrations()` - Waits for schema to be current (reader app)
   - `is_database_up_to_date()` - Checks schema version
   - Migration status tracking table

2. **`alembic/`** - Alembic migration directory
   - `env.py` - Configured for async SQLAlchemy support
   - `versions/` - Migration scripts directory
   - `alembic.ini` - Alembic configuration

3. **Modified Apps**:
   - `startdb.py` - Writer app that runs migrations before MQTT ingestion
   - `meshview/web.py` - Reader app that waits for schema updates

## How It Works - Automatic In-Place Updates

### ✨ Fully Automatic Operation

**No manual migration commands needed!** The database schema updates automatically when you:
1. Deploy new code with migration files
2. Restart the applications

### Writer App (startdb.py) Startup Sequence

1. Initialize database connection
2. Create migration status tracking table
3. Set "migration in progress" flag
4. **🔄 Automatically run any pending Alembic migrations** (synchronously)
   - Detects current schema version
   - Compares to latest available migration
   - Runs all pending migrations in sequence
   - Updates database schema in place
5. Clear "migration in progress" flag
6. Start MQTT ingestion and other tasks

### Reader App (web.py) Startup Sequence

1. Initialize database connection
2. **Check database schema version**
3. If not up to date:
   - Wait up to 60 seconds (30 retries × 2 seconds)
   - Check every 2 seconds for schema updates
   - Automatically proceeds once writer completes migrations
4. Once schema is current, start web server

### 🎯 Key Point: Zero Manual Steps

When you deploy new code with migrations:
```bash
# Just start the apps - migrations happen automatically!
./env/bin/python startdb.py  # Migrations run here automatically
./env/bin/python main.py     # Waits for migrations, then starts
```

**The database updates itself!** No need to run `alembic upgrade` manually.

### Coordination

The apps coordinate using:
- **Alembic version table** (`alembic_version`) - Tracks current schema version
- **Migration status table** (`migration_status`) - Optional flag for "in progress" state

## Creating New Migrations

### Using the helper script:

```bash
./env/bin/python create_migration.py
```

### Manual creation:

```bash
./env/bin/alembic revision --autogenerate -m "Description of changes"
```

This will:
1. Compare current database schema with SQLAlchemy models
2. Generate a migration script in `alembic/versions/`
3. Automatically detect most schema changes

### Manual migration (advanced):

```bash
./env/bin/alembic revision -m "Manual migration"
```

Then edit the generated file to add custom migration logic.

## Running Migrations

### Automatic (Recommended)

Migrations run automatically when the writer app starts:

```bash
./env/bin/python startdb.py
```

### Manual

To run migrations manually:

```bash
./env/bin/alembic upgrade head
```

To downgrade:

```bash
./env/bin/alembic downgrade -1  # Go back one version
./env/bin/alembic downgrade base  # Go back to beginning
```

## Checking Migration Status

Check current database version:

```bash
./env/bin/alembic current
```

View migration history:

```bash
./env/bin/alembic history
```

## Benefits

1. **Zero Manual Intervention**: Migrations run automatically on startup
2. **Safe Coordination**: Reader won't connect to incompatible schema
3. **Version Control**: All schema changes tracked in git
4. **Rollback Capability**: Can downgrade if needed
5. **Auto-generation**: Most migrations created automatically from model changes

## Migration Workflow

### Development Process

1. **Modify SQLAlchemy models** in `meshview/models.py`
2. **Create migration**:
   ```bash
   ./env/bin/python create_migration.py
   ```
3. **Review generated migration** in `alembic/versions/`
4. **Test migration**:
   - Stop all apps
   - Start writer app (migrations run automatically)
   - Start reader app (waits for schema to be current)
5. **Commit migration** to version control

### Production Deployment

1. **Deploy new code** with migration scripts
2. **Start writer app** - Migrations run automatically
3. **Start reader app** - Waits for migrations, then starts
4. **Monitor logs** for migration success

## Troubleshooting

### Migration fails

Check logs in writer app for error details. To manually fix:

```bash
./env/bin/alembic current  # Check current version
./env/bin/alembic history  # View available versions
./env/bin/alembic upgrade head  # Try manual upgrade
```

### Reader app won't start (timeout)

Check if writer app is running and has completed migrations:

```bash
./env/bin/alembic current
```

### Reset to clean state

⚠️ **Warning: This will lose all data**

```bash
rm packets.db  # Or your database file
./env/bin/alembic upgrade head  # Create fresh schema
```

## File Structure

```
meshview/
├── alembic.ini                 # Alembic configuration
├── alembic/
│   ├── env.py                  # Async-enabled migration runner
│   ├── script.py.mako          # Migration template
│   └── versions/               # Migration scripts
│       └── c88468b7ab0b_initial_migration.py
├── meshview/
│   ├── models.py               # SQLAlchemy models (source of truth)
│   ├── migrations.py           # Migration utilities
│   ├── mqtt_database.py        # Writer database connection
│   └── database.py             # Reader database connection
├── startdb.py                  # Writer app (runs migrations)
├── main.py                     # Entry point for reader app
└── create_migration.py         # Helper script for creating migrations
```

## Configuration

Database URL is read from `config.ini`:

```ini
[database]
connection_string = sqlite+aiosqlite:///packets.db
```

Alembic automatically uses this configuration through `meshview/migrations.py`.

## Important Notes

1. **Always test migrations** in development before deploying to production
2. **Backup database** before running migrations in production
3. **Check for data loss** - Some migrations may require data migration logic
4. **Coordinate deployments** - Start writer before readers in multi-instance setups
5. **Monitor logs** during first startup after deployment

## Example Migrations

### Example 1: Generated Initial Migration

Here's what an auto-generated migration looks like (from comparing models to database):

```python
"""Initial migration

Revision ID: c88468b7ab0b
Revises: 
Create Date: 2025-01-26 20:56:50.123456

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'c88468b7ab0b'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Upgrade operations
    op.create_table('node',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('node_id', sa.BigInteger(), nullable=True),
        # ... more columns
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # Downgrade operations
    op.drop_table('node')
```

### Example 2: Manual Migration Adding a New Table

We've included an example migration (`1717fa5c6545_add_example_table.py`) that demonstrates how to manually create a new table:

```python
"""Add example table

Revision ID: 1717fa5c6545
Revises: c88468b7ab0b
Create Date: 2025-10-26 20:59:04.347066
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    """Create example table with sample columns."""
    op.create_table(
        'example',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                  server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create an index on the name column for faster lookups
    op.create_index('idx_example_name', 'example', ['name'])

def downgrade() -> None:
    """Remove example table."""
    op.drop_index('idx_example_name', table_name='example')
    op.drop_table('example')
```

**Key features demonstrated:**
- Various column types (Integer, String, Text, Float, Boolean, DateTime)
- Primary key with autoincrement
- Nullable and non-nullable columns
- Server defaults (for timestamps and booleans)
- Creating indexes
- Proper downgrade that reverses all changes

**To test this migration:**

```bash
# Apply the migration
./env/bin/alembic upgrade head

# Check it was applied
./env/bin/alembic current

# Verify table was created
sqlite3 packetsPL.db "SELECT sql FROM sqlite_master WHERE type='table' AND name='example';"

# Roll back the migration
./env/bin/alembic downgrade -1

# Verify table was removed
sqlite3 packetsPL.db "SELECT name FROM sqlite_master WHERE type='table' AND name='example';"
```

**To remove this example migration** (after testing):

```bash
# First make sure you're not on this revision
./env/bin/alembic downgrade c88468b7ab0b

# Then delete the migration file
rm alembic/versions/1717fa5c6545_add_example_table.py
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Async SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)