#!/usr/bin/env python3
"""
Script to create a blank migration for manual editing.

Usage:
    ./env/bin/python create_example_migration.py

This creates an empty migration file that you can manually edit to add
custom migration logic (data migrations, complex schema changes, etc.)

Unlike create_migration.py which auto-generates from model changes,
this creates a blank template for you to fill in.
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

# Generate blank migration
try:
    print("Creating blank migration for manual editing...")
    command.revision(alembic_cfg, autogenerate=False, message="Manual migration")
    print("✓ Successfully created blank migration!")
    print("\nNow edit the generated file in alembic/versions/")
    print("Add your custom upgrade() and downgrade() logic")
except Exception as e:
    print(f"✗ Error creating migration: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
