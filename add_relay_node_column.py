"""
Migration script to add relay_node column to packet_seen table.
Run this once to update your database schema.
"""
import asyncio
from meshview import database

async def add_relay_node_column():
    """Add relay_node column to packet_seen table"""
    async with database.async_session() as session:
        # Add the column
        await session.execute("""
            ALTER TABLE packet_seen 
            ADD COLUMN IF NOT EXISTS relay_node BIGINT
        """)
        await session.commit()
        print("Successfully added relay_node column to packet_seen table")

if __name__ == "__main__":
    asyncio.run(add_relay_node_column())
