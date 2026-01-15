from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshview import models


def init_database(database_connection_string):
    global engine, async_session
    url = make_url(database_connection_string)
    kwargs = {"echo": False}
    if url.drivername.startswith("sqlite"):
        kwargs["connect_args"] = {"timeout": 900}
    engine = create_async_engine(url, **kwargs)
    async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
