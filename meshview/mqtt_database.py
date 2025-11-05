from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshview import models


def init_database(database_connection_string):
    global engine, async_session
    engine = create_async_engine(
        database_connection_string, echo=False, connect_args={"timeout": 900}
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
