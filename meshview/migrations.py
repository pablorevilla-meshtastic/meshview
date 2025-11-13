"""
Database migration management for MeshView.

This module provides utilities for:
- Running Alembic migrations programmatically
- Checking database schema versions
- Coordinating migrations between writer and reader apps
"""

import asyncio
import logging
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import command

logger = logging.getLogger(__name__)


def get_alembic_config(database_url: str) -> Config:
    """
    Get Alembic configuration with the database URL set.

    Args:
        database_url: SQLAlchemy database connection string

    Returns:
        Configured Alembic Config object
    """
    # Get the alembic.ini path (in project root)
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"

    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)

    return config


async def get_current_revision(engine: AsyncEngine) -> str | None:
    """
    Get the current database schema revision.

    Args:
        engine: Async SQLAlchemy engine

    Returns:
        Current revision string, or None if no migrations applied
    """
    async with engine.connect() as connection:

        def _get_revision(conn):
            context = MigrationContext.configure(conn)
            return context.get_current_revision()

        revision = await connection.run_sync(_get_revision)
        return revision


async def get_head_revision(database_url: str) -> str | None:
    """
    Get the head (latest) revision from migration scripts.

    Args:
        database_url: Database connection string

    Returns:
        Head revision string, or None if no migrations exist
    """
    config = get_alembic_config(database_url)
    script_dir = ScriptDirectory.from_config(config)

    head = script_dir.get_current_head()
    return head


async def is_database_up_to_date(engine: AsyncEngine, database_url: str) -> bool:
    """
    Check if database is at the latest schema version.

    Args:
        engine: Async SQLAlchemy engine
        database_url: Database connection string

    Returns:
        True if database is up to date, False otherwise
    """
    current = await get_current_revision(engine)
    head = await get_head_revision(database_url)

    # If there are no migrations yet, consider it up to date
    if head is None:
        return True

    return current == head


def run_migrations(database_url: str) -> None:
    """
    Run all pending migrations to bring database up to date.

    This is a synchronous operation that runs Alembic migrations.
    Should be called by the writer app on startup.

    Args:
        database_url: Database connection string
    """
    logger.info("Running database migrations...")
    import sys

    sys.stdout.flush()

    config = get_alembic_config(database_url)

    try:
        # Run migrations to head
        logger.info("Calling alembic upgrade command...")
        sys.stdout.flush()
        command.upgrade(config, "head")
        logger.info("Database migrations completed successfully")
        sys.stdout.flush()
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        raise


async def wait_for_migrations(
    engine: AsyncEngine, database_url: str, max_retries: int = 30, retry_delay: int = 2
) -> bool:
    """
    Wait for database migrations to complete.

    This should be called by the reader app to wait until
    the database schema is up to date before proceeding.

    Args:
        engine: Async SQLAlchemy engine
        database_url: Database connection string
        max_retries: Maximum number of retry attempts
        retry_delay: Seconds to wait between retries

    Returns:
        True if database is up to date, False if max retries exceeded
    """
    for attempt in range(max_retries):
        try:
            if await is_database_up_to_date(engine, database_url):
                logger.info("Database schema is up to date")
                return True

            current = await get_current_revision(engine)
            head = await get_head_revision(database_url)

            logger.info(
                f"Database schema not up to date (current: {current}, head: {head}). "
                f"Waiting... (attempt {attempt + 1}/{max_retries})"
            )

            await asyncio.sleep(retry_delay)

        except Exception as e:
            logger.warning(
                f"Error checking database version (attempt {attempt + 1}/{max_retries}): {e}"
            )
            await asyncio.sleep(retry_delay)

    logger.error(f"Database schema not up to date after {max_retries} attempts")
    return False


async def create_migration_status_table(engine: AsyncEngine) -> None:
    """
    Create a simple status table for migration coordination.

    This table can be used to signal when migrations are in progress.

    Args:
        engine: Async SQLAlchemy engine
    """
    async with engine.begin() as conn:
        await conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS migration_status (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                in_progress BOOLEAN NOT NULL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        )

        # Insert initial row if not exists
        await conn.execute(
            text("""
            INSERT OR IGNORE INTO migration_status (id, in_progress)
            VALUES (1, 0)
        """)
        )


async def set_migration_in_progress(engine: AsyncEngine, in_progress: bool) -> None:
    """
    Set the migration in-progress flag.

    Args:
        engine: Async SQLAlchemy engine
        in_progress: True if migration is in progress, False otherwise
    """
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                UPDATE migration_status
                SET in_progress = :in_progress,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """),
            {"in_progress": in_progress},
        )


async def is_migration_in_progress(engine: AsyncEngine) -> bool:
    """
    Check if a migration is currently in progress.

    Args:
        engine: Async SQLAlchemy engine

    Returns:
        True if migration is in progress, False otherwise
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT in_progress FROM migration_status WHERE id = 1")
            )
            row = result.fetchone()
            return bool(row[0]) if row else False
    except Exception:
        # If table doesn't exist or query fails, assume no migration in progress
        return False
