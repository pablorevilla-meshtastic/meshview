"""Persist reported altitudes without losing them when a report omits altitude."""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from meshtastic.protobuf.mesh_pb2 import Position
from meshtastic.protobuf.mqtt_pb2 import MapReport, ServiceEnvelope
from meshtastic.protobuf.portnums_pb2 import PortNum
from meshview import mqtt_database, mqtt_store
from meshview.models import Base, Node


@pytest.mark.asyncio
@pytest.mark.parametrize("report_type", [Position, MapReport])
async def test_altitude_updates(monkeypatch, report_type):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(mqtt_database, "async_session", sessions, raising=False)
    monkeypatch.setattr(mqtt_store, "MQTT_GATEWAY_CACHE", set())
    port = PortNum.POSITION_APP if report_type is Position else PortNum.MAP_REPORT_APP
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        cases = [
            (None, 200000000, None),
            (125, 200000000, 125),
            (None, 200000000, 125),
            (-30, 200000000, -30),
            (900, 0, -30),  # Invalid location must not update altitude.
            (0, 200000000, 0 if report_type is Position else -30),
        ]
        for packet_id, (altitude, coordinate, expected) in enumerate(cases, start=1):
            report = report_type(latitude_i=coordinate, longitude_i=coordinate)
            if altitude is not None:
                report.altitude = altitude
            env = ServiceEnvelope(gateway_id="!00000002", channel_id="test")
            env.packet.id = packet_id
            setattr(env.packet, "from", 123)
            env.packet.decoded.portnum = port
            env.packet.decoded.payload = report.SerializeToString()
            await mqtt_store.process_envelope("test", env)
            async with sessions() as session:
                node = (await session.execute(select(Node).where(Node.node_id == 123))).scalar_one()
                assert node.last_altitude == expected
                assert node.to_dict()["last_altitude"] == expected
    finally:
        await engine.dispose()
