from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import event

from meshview import models


def init_database(database_connection_string):
    global engine, async_session

    url = make_url(database_connection_string)
    kwargs = {"echo": False}

    if url.drivername.startswith("sqlite"):
        kwargs["connect_args"] = {"timeout": 900}  # seconds

    engine = create_async_engine(url, **kwargs)

    # Enforce SQLite pragmas on every new DB connection
    if url.drivername.startswith("sqlite"):

        @event.listens_for(engine.sync_engine, "connect")
        def _set_sqlite_pragmas(dbapi_conn, _):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA busy_timeout=900000;")  # ms
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.close()

    async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
