from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from meshview import models

engine = None
async_session = None


def init_database(database_connection_string):
    global engine, async_session
    kwargs = {"echo": False}

    # Apply SQLite-specific settings only for SQLite databases
    if 'sqlite' in database_connection_string.lower():
        # Ensure SQLite is opened in read-only mode
        database_connection_string += "?mode=ro"
        kwargs["connect_args"] = {"uri": True}

    engine = create_async_engine(database_connection_string, **kwargs)
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
