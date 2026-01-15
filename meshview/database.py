from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from meshview import models

engine = None
async_session = None


def init_database(database_connection_string):
    global engine, async_session
    kwargs = {"echo": False}
    url = make_url(database_connection_string)
    connect_args = {}

    if url.drivername.startswith("sqlite"):
        query = dict(url.query)
        query.setdefault("mode", "ro")
        url = url.set(query=query)
        connect_args["uri"] = True

    if connect_args:
        kwargs["connect_args"] = connect_args

    engine = create_async_engine(url, **kwargs)
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
