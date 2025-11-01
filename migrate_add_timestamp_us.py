#!/usr/bin/env python3
"""
Migration script to add microsecond timestamp columns to existing database.

This script implements the changes described in GitHub issue #55:
- Adds import_time_us INTEGER columns to packet, packet_seen, and traceroute tables
- Populates the new columns from existing import_time datetime values
- Creates indexes on the new columns for performance

Usage:
    python migrate_add_timestamp_us.py [database_path]

If database_path is not provided, it will use 'packets.db' in the current directory.
"""

import asyncio
import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


async def migrate_database(db_path: str):
    """Run the migration to add microsecond timestamp columns."""

    print(f"Starting migration for database: {db_path}")

    # Create async engine
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Check if columns already exist
        print("\nChecking if migration is needed...")
        result = await session.execute(text("PRAGMA table_info(packet)"))
        columns = [row[1] for row in result.fetchall()]

        if 'import_time_us' in columns:
            print("Migration already applied - import_time_us column already exists")
            return

        print("\n=== Step 1: Adding new columns ===")

        # Add import_time_us column to packet table
        print("Adding import_time_us to packet table...")
        await session.execute(text("ALTER TABLE packet ADD COLUMN import_time_us INTEGER"))
        await session.commit()

        # Add import_time_us column to packet_seen table
        print("Adding import_time_us to packet_seen table...")
        await session.execute(text("ALTER TABLE packet_seen ADD COLUMN import_time_us INTEGER"))
        await session.commit()

        # Add import_time_us column to traceroute table
        print("Adding import_time_us to traceroute table...")
        await session.execute(text("ALTER TABLE traceroute ADD COLUMN import_time_us INTEGER"))
        await session.commit()

        print("\n=== Step 2: Populating new columns from existing data ===")

        # Populate packet.import_time_us
        print("Populating packet.import_time_us...")
        # Note: import_time is stored as local time text, but we convert to UTC timestamp
        # strftime('%s', ...) interprets the datetime as UTC
        await session.execute(
            text("""
            UPDATE packet
            SET import_time_us = 
                CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
            WHERE import_time IS NOT NULL
        """)
        )
        await session.commit()

        # Get count for verification
        result = await session.execute(
            text("SELECT COUNT(*) FROM packet WHERE import_time_us IS NOT NULL")
        )
        count = result.scalar()
        print(f"  Updated {count} packet records")

        # Populate packet_seen.import_time_us
        print("Populating packet_seen.import_time_us...")
        await session.execute(
            text("""
            UPDATE packet_seen
            SET import_time_us = 
                CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
            WHERE import_time IS NOT NULL
        """)
        )
        await session.commit()

        result = await session.execute(
            text("SELECT COUNT(*) FROM packet_seen WHERE import_time_us IS NOT NULL")
        )
        count = result.scalar()
        print(f"  Updated {count} packet_seen records")

        # Populate traceroute.import_time_us
        print("Populating traceroute.import_time_us...")
        await session.execute(
            text("""
            UPDATE traceroute
            SET import_time_us = 
                CAST((strftime('%s', import_time) || substr(import_time, 21, 6)) AS INTEGER)
            WHERE import_time IS NOT NULL
        """)
        )
        await session.commit()

        result = await session.execute(
            text("SELECT COUNT(*) FROM traceroute WHERE import_time_us IS NOT NULL")
        )
        count = result.scalar()
        print(f"  Updated {count} traceroute records")

        print("\n=== Step 3: Creating indexes ===")

        # Create indexes on the new columns
        print("Creating index on packet.import_time_us...")
        await session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_packet_import_time_us ON packet(import_time_us DESC)"
            )
        )
        await session.commit()

        print("Creating composite index on packet(from_node_id, import_time_us)...")
        await session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_packet_from_node_time_us ON packet(from_node_id, import_time_us DESC)"
            )
        )
        await session.commit()

        print("Creating index on packet_seen.import_time_us...")
        await session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_packet_seen_import_time_us ON packet_seen(import_time_us)"
            )
        )
        await session.commit()

        print("Creating index on traceroute.import_time_us...")
        await session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_traceroute_import_time_us ON traceroute(import_time_us)"
            )
        )
        await session.commit()

        print("\n=== Migration completed successfully! ===")
        print("\nVerification:")

        # Verify the migration
        result = await session.execute(
            text("""
            SELECT 
                COUNT(*) as total,
                COUNT(import_time_us) as with_us_timestamp
            FROM packet
        """)
        )
        row = result.fetchone()
        print(f"  Packet table: {row[1]}/{row[0]} records have microsecond timestamps")

        result = await session.execute(
            text("""
            SELECT 
                COUNT(*) as total,
                COUNT(import_time_us) as with_us_timestamp
            FROM packet_seen
        """)
        )
        row = result.fetchone()
        print(f"  PacketSeen table: {row[1]}/{row[0]} records have microsecond timestamps")

        result = await session.execute(
            text("""
            SELECT 
                COUNT(*) as total,
                COUNT(import_time_us) as with_us_timestamp
            FROM traceroute
        """)
        )
        row = result.fetchone()
        print(f"  Traceroute table: {row[1]}/{row[0]} records have microsecond timestamps")

    await engine.dispose()


def main():
    # Get database path from command line or use default
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "packets.db"

    # Check if database exists
    if not Path(db_path).exists():
        print(f"Error: Database file not found: {db_path}")
        sys.exit(1)

    # Run the migration
    asyncio.run(migrate_database(db_path))


if __name__ == "__main__":
    main()
