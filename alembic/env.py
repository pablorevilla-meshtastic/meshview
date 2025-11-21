import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import models metadata for autogenerate support
from meshview.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# Use disable_existing_loggers=False to preserve app logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode."""
    # Get configuration section
    configuration = config.get_section(config.config_ini_section, {})

    # If sqlalchemy.url is not set in alembic.ini, try to get it from meshview config
    if "sqlalchemy.url" not in configuration:
        try:
            from meshview.config import CONFIG

            configuration["sqlalchemy.url"] = CONFIG["database"]["connection_string"]
        except Exception:
            # Fallback to a default for initial migration creation
            configuration["sqlalchemy.url"] = "sqlite+aiosqlite:///packets.db"

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async support."""
    try:
        # Event loop is already running, schedule and run the coroutine
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.submit(lambda: asyncio.run(run_async_migrations())).result()
    except RuntimeError:
        # No event loop running, create one
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
