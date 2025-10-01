from meshview import models
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = None
async_session = None


def init_database(database_connection_string):
    global engine, async_session
    kwargs = {"echo": False}
    # Ensure SQLite is opened in read-only mode
    database_connection_string += "?mode=ro"
    kwargs["connect_args"] = {"uri": True}
    engine = create_async_engine(database_connection_string, **kwargs)
    async_session = async_sessionmaker( bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
