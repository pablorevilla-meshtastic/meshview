# Database Changes With Alembic

This guide explains how to make database schema changes in MeshView using Alembic migrations.

## Overview

When you need to add, modify, or remove columns from database tables, you must:
1. Update the SQLAlchemy model
2. Create an Alembic migration
3. Let the system automatically apply the migration

## Step-by-Step Process

### 1. Update the Model

Edit `meshview/models.py` to add/modify the column in the appropriate model class:

```python
class Traceroute(Base):
    __tablename__ = "traceroute"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # ... existing columns ...
    route_return: Mapped[bytes] = mapped_column(nullable=True)  # New column
```

### 2. Create an Alembic Migration

Generate a new migration file with a descriptive message:

```bash
./env/bin/alembic revision -m "add route_return to traceroute"
```

This creates a new file in `alembic/versions/` with a unique revision ID.

### 3. Fill in the Migration

Edit the generated migration file to implement the actual database changes:

```python
def upgrade() -> None:
    # Add route_return column to traceroute table
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.add_column(sa.Column('route_return', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    # Remove route_return column from traceroute table
    with op.batch_alter_table('traceroute', schema=None) as batch_op:
        batch_op.drop_column('route_return')
```

### 4. Migration Runs Automatically

When you restart the application with `mvrun.py`:

1. The writer process (`startdb.py`) starts up
2. It checks if the database schema is up to date
3. If new migrations are pending, it runs them automatically
4. The reader process (web server) waits for migrations to complete before starting

**No manual migration command is needed** - the application handles this automatically on startup.

### 5. Commit Both Files

Add both files to git:

```bash
git add meshview/models.py
git add alembic/versions/ac311b3782a1_add_route_return_to_traceroute.py
git commit -m "Add route_return column to traceroute table"
```

## Important Notes

### SQLite Compatibility

Always use `batch_alter_table` for SQLite compatibility:

```python
with op.batch_alter_table('table_name', schema=None) as batch_op:
    batch_op.add_column(...)
```

SQLite has limited ALTER TABLE support, and `batch_alter_table` works around these limitations.

### Migration Process

- **Writer process** (`startdb.py`): Runs migrations on startup
- **Reader process** (web server in `main.py`): Waits for migrations to complete
- Migrations are checked and applied every time the application starts
- The system uses a migration status table to coordinate between processes

### Common Column Types

```python
# Integer
column: Mapped[int] = mapped_column(BigInteger, nullable=True)

# String
column: Mapped[str] = mapped_column(nullable=True)

# Bytes/Binary
column: Mapped[bytes] = mapped_column(nullable=True)

# DateTime
column: Mapped[datetime] = mapped_column(nullable=True)

# Boolean
column: Mapped[bool] = mapped_column(nullable=True)

# Float
column: Mapped[float] = mapped_column(nullable=True)
```

### Migration File Location

Migrations are stored in: `alembic/versions/`

Each migration file includes:
- Revision ID (unique identifier)
- Down revision (previous migration in chain)
- Create date
- `upgrade()` function (applies changes)
- `downgrade()` function (reverts changes)

## Troubleshooting

### Migration Not Running

If migrations don't run automatically:

1. Check that the database is writable
2. Look for errors in the startup logs
3. Verify the migration chain is correct (each migration references the previous one)

### Manual Migration (Not Recommended)

If you need to manually run migrations for debugging:

```bash
./env/bin/alembic upgrade head
```

However, the application normally handles this automatically.
