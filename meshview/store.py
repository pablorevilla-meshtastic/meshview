from datetime import datetime, timedelta

from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.orm import lazyload

from meshview import database, models
from meshview.models import Node, Packet, PacketSeen, Traceroute


async def get_node(node_id):
    async with database.async_session() as session:
        result = await session.execute(select(Node).where(Node.node_id == node_id))
        return result.scalar_one_or_none()


async def get_fuzzy_nodes(query):
    async with database.async_session() as session:
        q = select(Node).where(
            Node.id.ilike(query + "%")
            | Node.long_name.ilike(query + "%")
            | Node.short_name.ilike(query + "%")
        )
        result = await session.execute(q)
        return result.scalars()


async def get_packets(
    from_node_id=None,
    to_node_id=None,
    node_id=None,  # legacy: match either from OR to
    portnum=None,
    after=None,
    contains=None,  # NEW: SQL-level substring match
    limit=50,
):
    """
    SQLAlchemy 2.0 async ORM version.
    Supports strict from/to/node filtering, substring payload search,
    portnum, since, and limit.
    """

    async with database.async_session() as session:
        stmt = select(models.Packet)
        conditions = []

        # Strict FROM filter
        if from_node_id is not None:
            conditions.append(models.Packet.from_node_id == from_node_id)

        # Strict TO filter
        if to_node_id is not None:
            conditions.append(models.Packet.to_node_id == to_node_id)

        # Legacy node ID filter: match either direction
        if node_id is not None:
            conditions.append(
                or_(models.Packet.from_node_id == node_id, models.Packet.to_node_id == node_id)
            )

        # Port filter
        if portnum is not None:
            conditions.append(models.Packet.portnum == portnum)

        # Timestamp filter
        if after is not None:
            conditions.append(models.Packet.import_time_us > after)

        # Case-insensitive substring search on UTF-8 payload (stored as BLOB)
        if contains:
            contains_lower = contains.lower()
            conditions.append(func.lower(models.Packet.payload).like(f"%{contains_lower}%"))

        # Apply all conditions
        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Order newest → oldest
        stmt = stmt.order_by(models.Packet.import_time_us.desc())

        # Apply limit
        stmt = stmt.limit(limit)

        # Execute query
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_packets_from(node_id=None, portnum=None, since=None, limit=500):
    async with database.async_session() as session:
        q = select(Packet)

        if node_id:
            q = q.where(Packet.from_node_id == node_id)
        if portnum:
            q = q.where(Packet.portnum == portnum)
        if since:
            q = q.where(Packet.import_time > (datetime.now() - since))
        result = await session.execute(q.limit(limit).order_by(Packet.import_time.desc()))
        return result.scalars()


async def get_packet(packet_id):
    async with database.async_session() as session:
        q = select(Packet).where(Packet.id == packet_id)
        result = await session.execute(q)
        return result.scalar_one_or_none()


async def get_packets_seen(packet_id):
    async with database.async_session() as session:
        result = await session.execute(
            select(PacketSeen)
            .where(PacketSeen.packet_id == packet_id)
            .order_by(PacketSeen.import_time.desc())
        )
        return result.scalars()


async def has_packets(node_id, portnum):
    async with database.async_session() as session:
        return bool(
            (
                await session.execute(
                    select(Packet.id).where(Packet.from_node_id == node_id).limit(1)
                )
            ).scalar()
        )


async def get_traceroute(packet_id):
    async with database.async_session() as session:
        result = await session.execute(
            select(Traceroute)
            .where(Traceroute.packet_id == packet_id)
            .order_by(Traceroute.import_time)
        )
        return result.scalars()


async def get_traceroutes(since):
    async with database.async_session() as session:
        stmt = (
            select(Traceroute)
            .join(Packet)
            .where(Traceroute.import_time > since)
            .order_by(Traceroute.import_time)
        )
        stream = await session.stream_scalars(stmt)
        async for tr in stream:
            yield tr


async def get_mqtt_neighbors(since):
    async with database.async_session() as session:
        result = await session.execute(
            select(PacketSeen, Packet)
            .join(Packet)
            .where(
                (PacketSeen.hop_limit == PacketSeen.hop_start)
                & (PacketSeen.hop_start != 0)
                & (PacketSeen.import_time > (datetime.now() - since))
            )
            .options(
                lazyload(Packet.from_node),
                lazyload(Packet.to_node),
            )
        )
        return result


async def get_total_node_count(channel: str = None) -> int:
    try:
        async with database.async_session() as session:
            q = select(func.count(Node.id)).where(
                Node.last_update > datetime.now() - timedelta(days=1)
            )

            if channel:
                q = q.where(Node.channel == channel)

            result = await session.execute(q)
            return result.scalar()
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


async def get_top_traffic_nodes():
    try:
        async with database.async_session() as session:
            result = await session.execute(
                text("""
                SELECT 
                    n.node_id,
                    n.long_name,
                    n.short_name,
                    n.channel,
                    COUNT(DISTINCT p.id) AS total_packets_sent,
                    COUNT(ps.packet_id) AS total_times_seen
                FROM node n
                LEFT JOIN packet p ON n.node_id = p.from_node_id
                    AND p.import_time >= DATETIME('now', 'localtime', '-24 hours')
                LEFT JOIN packet_seen ps ON p.id = ps.packet_id
                GROUP BY n.node_id, n.long_name, n.short_name
                HAVING total_packets_sent > 0
                ORDER BY total_times_seen DESC;
            """)
            )

            rows = result.fetchall()

            nodes = [
                {
                    'node_id': row[0],
                    'long_name': row[1],
                    'short_name': row[2],
                    'channel': row[3],
                    'total_packets_sent': row[4],
                    'total_times_seen': row[5],
                }
                for row in rows
            ]
            return nodes

    except Exception as e:
        print(f"Error retrieving top traffic nodes: {str(e)}")
        return []


async def get_node_traffic(node_id: int):
    try:
        async with database.async_session() as session:
            result = await session.execute(
                text("""
                    SELECT 
                        node.long_name, packet.portnum, 
                        COUNT(*) AS packet_count
                    FROM packet
                    JOIN node ON packet.from_node_id = node.node_id
                    WHERE node.node_id = :node_id 
                    AND packet.import_time >= DATETIME('now', 'localtime', '-24 hours') 
                    GROUP BY packet.portnum
                    ORDER BY packet_count DESC;
                """),
                {"node_id": node_id},
            )

            # Map the result to include node.long_name and packet data
            traffic_data = [
                {
                    "long_name": row[0],  # node.long_name
                    "portnum": row[1],  # packet.portnum
                    "packet_count": row[2],  # COUNT(*) as packet_count
                }
                for row in result.all()
            ]

            return traffic_data

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error fetching node traffic: {str(e)}")
        return []


async def get_nodes(role=None, channel=None, hw_model=None, days_active=None):
    """
    Fetches nodes from the database based on optional filtering criteria.

    Parameters:
        role (str, optional): The role of the node (converted to uppercase for consistency).
        channel (str, optional): The communication channel associated with the node.
        hw_model (str, optional): The hardware model of the node.

    Returns:
        list: A list of Node objects that match the given criteria.
    """
    try:
        async with database.async_session() as session:
            # print(channel)  # Debugging output (consider replacing with logging)

            # Start with a base query selecting all nodes
            query = select(Node)

            # Apply filters based on provided parameters
            if role is not None:
                query = query.where(Node.role == role.upper())  # Ensure role is uppercase
            if channel is not None:
                query = query.where(Node.channel == channel)
            if hw_model is not None:
                query = query.where(Node.hw_model == hw_model)

            if days_active is not None:
                query = query.where(Node.last_update > datetime.now() - timedelta(days_active))

            # Exclude nodes where last_update is an empty string
            query = query.where(Node.last_update != "")

            # Order results by long_name in ascending order
            query = query.order_by(Node.short_name.asc())

            # Execute the query and retrieve results
            result = await session.execute(query)
            nodes = result.scalars().all()
            return nodes  # Return the list of nodes

    except Exception:
        print("error reading DB")  # Consider using logging instead of print
        return []  # Return an empty list in case of failure


async def get_packet_stats(
    period_type: str = "day",
    length: int = 14,
    channel: str | None = None,
    portnum: int | None = None,
    to_node: int | None = None,
    from_node: int | None = None,
):
    now = datetime.now()

    if period_type == "hour":
        start_time = now - timedelta(hours=length)
        time_format = '%Y-%m-%d %H:00'
    elif period_type == "day":
        start_time = now - timedelta(days=length)
        time_format = '%Y-%m-%d'
    else:
        raise ValueError("period_type must be 'hour' or 'day'")

    async with database.async_session() as session:
        q = select(
            func.strftime(time_format, Packet.import_time).label('period'),
            func.count().label('count'),
        ).where(Packet.import_time >= start_time)

        # Filters
        if channel:
            q = q.where(func.lower(Packet.channel) == channel.lower())
        if portnum is not None:
            q = q.where(Packet.portnum == portnum)
        if to_node is not None:
            q = q.where(Packet.to_node_id == to_node)
        if from_node is not None:
            q = q.where(Packet.from_node_id == from_node)

        q = q.group_by('period').order_by('period')

        result = await session.execute(q)
        data = [{"period": row.period, "count": row.count} for row in result]

        return {
            "period_type": period_type,
            "length": length,
            "channel": channel,
            "portnum": portnum,
            "to_node": to_node,
            "from_node": from_node,
            "data": data,
        }


async def get_channels_in_period(period_type: str = "hour", length: int = 24):
    """
    Returns a sorted list of distinct channels used in packets over a given period.
    period_type: "hour" or "day"
    length: number of hours or days to look back
    """
    now_us = int(datetime.utcnow().timestamp() * 1_000_000)

    if period_type == "hour":
        delta_us = length * 3600 * 1_000_000
    elif period_type == "day":
        delta_us = length * 86400 * 1_000_000
    else:
        raise ValueError("period_type must be 'hour' or 'day'")

    start_us = now_us - delta_us

    async with database.async_session() as session:
        stmt = (
            select(Packet.channel)
            .where(Packet.import_time_us >= start_us)
            .distinct()
            .order_by(Packet.channel)
        )

        result = await session.execute(stmt)

        channels = [ch for ch in result.scalars().all() if ch is not None]

        return channels


async def get_total_packet_count(
    period_type: str | None = None,
    length: int | None = None,
    channel: str | None = None,
    from_node: int | None = None,
    to_node: int | None = None,
):
    """
    Count total packets, with ALL filters optional.
    If no filters -> return ALL packets ever.
    Uses import_time_us (microseconds).
    """

    # CASE 1: no filters -> count everything
    if (
        period_type is None
        and length is None
        and channel is None
        and from_node is None
        and to_node is None
    ):
        async with database.async_session() as session:
            q = select(func.count(Packet.id))
            res = await session.execute(q)
            return res.scalar() or 0

    # CASE 2: filtered mode -> compute time window using import_time_us
    now_us = int(datetime.now().timestamp() * 1_000_000)

    if period_type is None:
        period_type = "day"
    if length is None:
        length = 1

    if period_type == "hour":
        start_time_us = now_us - (length * 3600 * 1_000_000)
    elif period_type == "day":
        start_time_us = now_us - (length * 86400 * 1_000_000)
    else:
        raise ValueError("period_type must be 'hour' or 'day'")

    async with database.async_session() as session:
        q = select(func.count(Packet.id)).where(Packet.import_time_us >= start_time_us)

        if channel:
            q = q.where(func.lower(Packet.channel) == channel.lower())
        if from_node:
            q = q.where(Packet.from_node_id == from_node)
        if to_node:
            q = q.where(Packet.to_node_id == to_node)

        res = await session.execute(q)
        return res.scalar() or 0


async def get_total_packet_seen_count(
    packet_id: int | None = None,
    period_type: str | None = None,
    length: int | None = None,
    channel: str | None = None,
    from_node: int | None = None,
    to_node: int | None = None,
):
    """
    Count total PacketSeen rows.
    - If packet_id is provided -> count only that packet's seen entries.
    - Otherwise match EXACT SAME FILTERS as get_total_packet_count.
    Uses import_time_us for time window.
    """

    # SPECIAL CASE: direct packet_id lookup
    if packet_id is not None:
        async with database.async_session() as session:
            q = select(func.count(PacketSeen.packet_id)).where(PacketSeen.packet_id == packet_id)
            res = await session.execute(q)
            return res.scalar() or 0

    # No filters -> return ALL seen entries
    if (
        period_type is None
        and length is None
        and channel is None
        and from_node is None
        and to_node is None
    ):
        async with database.async_session() as session:
            q = select(func.count(PacketSeen.packet_id))
            res = await session.execute(q)
            return res.scalar() or 0

    # Compute time window
    now_us = int(datetime.now().timestamp() * 1_000_000)

    if period_type is None:
        period_type = "day"
    if length is None:
        length = 1

    if period_type == "hour":
        start_time_us = now_us - (length * 3600 * 1_000_000)
    elif period_type == "day":
        start_time_us = now_us - (length * 86400 * 1_000_000)
    else:
        raise ValueError("period_type must be 'hour' or 'day'")

    # JOIN Packet so we can apply identical filters
    async with database.async_session() as session:
        q = (
            select(func.count(PacketSeen.packet_id))
            .join(Packet, Packet.id == PacketSeen.packet_id)
            .where(Packet.import_time_us >= start_time_us)
        )

        if channel:
            q = q.where(func.lower(Packet.channel) == channel.lower())
        if from_node:
            q = q.where(Packet.from_node_id == from_node)
        if to_node:
            q = q.where(Packet.to_node_id == to_node)

        res = await session.execute(q)
        return res.scalar() or 0
