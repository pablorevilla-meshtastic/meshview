#!/usr/bin/env python3
"""
Helper script to create Alembic migrations from SQLAlchemy model changes.

Usage:
    ./env/bin/python create_migration.py

This will:
1. Load your current models from meshview/models.py
2. Compare them to the current database schema
3. Auto-generate a migration with the detected changes
4. Save the migration to alembic/versions/

After running this, review the generated migration file before committing!
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alembic.config import Config

from alembic import command

# Create Alembic config
alembic_cfg = Config("alembic.ini")

# Set database URL from meshview config
try:
    from meshview.config import CONFIG

    database_url = CONFIG["database"]["connection_string"]
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    print(f"Using database URL from config: {database_url}")
except Exception as e:
    print(f"Warning: Could not load meshview config: {e}")
    print("Using default database URL")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite+aiosqlite:///packets.db")

# Generate migration
try:
    print("\nComparing models to current database schema...")
    print("Generating migration...\n")
    command.revision(alembic_cfg, autogenerate=True, message="Auto-generated migration")
    print("\n✓ Successfully created migration!")
    print("\nNext steps:")
    print("1. Review the generated file in alembic/versions/")
    print("2. Edit the migration message/logic if needed")
    print("3. Test the migration: ./env/bin/alembic upgrade head")
    print("4. Commit the migration file to version control")
except Exception as e:
    print(f"\n✗ Error creating migration: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
