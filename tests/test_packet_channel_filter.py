"""Reliability samples must select the newest packets within the main channel."""

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshview import database, models, store


@pytest.mark.asyncio
async def test_channel_filter_applies_before_limit(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "async_session", sessions)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        async with sessions() as session:
            session.add_all(
                [
                    models.Packet(
                        id=1, from_node_id=123, portnum=1, channel="Main", import_time_us=100
                    ),
                    models.Packet(
                        id=2, from_node_id=123, portnum=1, channel="Main", import_time_us=200
                    ),
                    models.Packet(
                        id=3, from_node_id=123, portnum=1, channel="Other", import_time_us=300
                    ),
                    models.Packet(
                        id=4, from_node_id=456, portnum=1, channel="Main", import_time_us=400
                    ),
                    models.Packet(
                        id=5, from_node_id=123, portnum=3, channel="Main", import_time_us=500
                    ),
                ]
            )
            await session.commit()
        packets = await store.get_packets(from_node_id=123, portnum=1, channel="Main", limit=2)
        assert [p.id for p in packets] == [2, 1]
        packets = await store.get_packets(from_node_id=123, portnum=1, limit=2)
        assert [p.id for p in packets] == [3, 2]
        assert await store.get_packets(from_node_id=123, channel="Unknown", limit=2) == []
    finally:
        await engine.dispose()
