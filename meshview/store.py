import logging
from datetime import datetime, timedelta

from sqlalchemy import Text, and_, cast, func, or_, select
from sqlalchemy.orm import lazyload

from meshview import database, models
from meshview.models import Node, Packet, PacketSeen, Traceroute

logger = logging.getLogger(__name__)


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
    node_id=None,  # legacy
    portnum=None,
    after=None,
    contains=None,  # substring search
    limit=50,
):
    async with database.async_session() as session:
        stmt = select(models.Packet)
        conditions = []

        # Strict FROM filter
        if from_node_id is not None:
            conditions.append(models.Packet.from_node_id == from_node_id)

        # Strict TO filter
        if to_node_id is not None:
            conditions.append(models.Packet.to_node_id == to_node_id)

        # Legacy node_id (either direction)
        if node_id is not None:
            conditions.append(
                or_(
                    models.Packet.from_node_id == node_id,
                    models.Packet.to_node_id == node_id,
                )
            )

        # Port filter
        if portnum is not None:
            conditions.append(models.Packet.portnum == portnum)

        # Timestamp filter using microseconds
        if after is not None:
            conditions.append(models.Packet.import_time_us > after)

        # Case-insensitive substring search on payload (BLOB → TEXT)
        if contains:
            contains_lower = f"%{contains.lower()}%"
            payload_text = cast(models.Packet.payload, Text)
            conditions.append(func.lower(payload_text).like(contains_lower))

        # Apply WHERE conditions
        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Order by newest first
        stmt = stmt.order_by(models.Packet.import_time_us.desc())

        # Limit
        stmt = stmt.limit(limit)

        # Run query
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
            now_us = int(datetime.now().timestamp() * 1_000_000)
            start_us = now_us - int(since.total_seconds() * 1_000_000)
            q = q.where(Packet.import_time_us > start_us)
        result = await session.execute(q.limit(limit).order_by(Packet.import_time_us.desc()))
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
            .order_by(PacketSeen.import_time_us.desc())
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
            .order_by(Traceroute.import_time_us)
        )
        return result.scalars()


async def get_traceroutes(since):
    if isinstance(since, datetime):
        since_us = int(since.timestamp() * 1_000_000)
    else:
        since_us = int(since)
    async with database.async_session() as session:
        stmt = (
            select(Traceroute)
            .where(Traceroute.import_time_us > since_us)
            .order_by(Traceroute.import_time_us)
        )
        stream = await session.stream_scalars(stmt)
        async for tr in stream:
            yield tr


async def get_mqtt_neighbors(since):
    now_us = int(datetime.now().timestamp() * 1_000_000)
    start_us = now_us - int(since.total_seconds() * 1_000_000)
    async with database.async_session() as session:
        result = await session.execute(
            select(PacketSeen, Packet)
            .join(Packet)
            .where(
                (PacketSeen.hop_limit == PacketSeen.hop_start)
                & (PacketSeen.hop_start != 0)
                & (PacketSeen.import_time_us > start_us)
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
            now_us = int(datetime.now(datetime.UTC).timestamp() * 1_000_000)
            cutoff_us = now_us - 86400 * 1_000_000
            q = select(func.count(Node.id)).where(Node.last_seen_us > cutoff_us)

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
            now_us = int(datetime.now(datetime.UTC).timestamp() * 1_000_000)
            cutoff_us = now_us - 86400 * 1_000_000
            total_packets_sent = func.count(func.distinct(Packet.id)).label("total_packets_sent")
            total_times_seen = func.count(PacketSeen.packet_id).label("total_times_seen")

            stmt = (
                select(
                    Node.node_id,
                    Node.long_name,
                    Node.short_name,
                    Node.channel,
                    total_packets_sent,
                    total_times_seen,
                )
                .select_from(Node)
                .outerjoin(
                    Packet,
                    (Packet.from_node_id == Node.node_id) & (Packet.import_time_us >= cutoff_us),
                )
                .outerjoin(PacketSeen, PacketSeen.packet_id == Packet.id)
                .group_by(Node.node_id, Node.long_name, Node.short_name, Node.channel)
                .having(total_packets_sent > 0)
                .order_by(total_times_seen.desc())
            )

            rows = (await session.execute(stmt)).all()

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
            now_us = int(datetime.now(datetime.UTC).timestamp() * 1_000_000)
            cutoff_us = now_us - 86400 * 1_000_000
            packet_count = func.count().label("packet_count")

            stmt = (
                select(Node.long_name, Packet.portnum, packet_count)
                .select_from(Packet)
                .join(Node, Packet.from_node_id == Node.node_id)
                .where(Node.node_id == node_id)
                .where(Packet.import_time_us >= cutoff_us)
                .group_by(Node.long_name, Packet.portnum)
                .order_by(packet_count.desc())
            )

            result = await session.execute(stmt)
            return [
                {
                    "long_name": row.long_name,
                    "portnum": row.portnum,
                    "packet_count": row.packet_count,
                }
                for row in result.all()
            ]

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error fetching node traffic: {str(e)}")
        return []


async def get_nodes(node_id=None, role=None, channel=None, hw_model=None, days_active=None):
    """
    Fetches nodes from the database based on optional filtering criteria.

    Parameters:
        node_id
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
            if node_id is not None:
                try:
                    node_id_int = int(node_id)
                except (TypeError, ValueError):
                    node_id_int = node_id
                query = query.where(Node.node_id == node_id_int)
            if role is not None:
                query = query.where(Node.role == role.upper())  # Ensure role is uppercase
            if channel is not None:
                query = query.where(Node.channel == channel)
            if hw_model is not None:
                query = query.where(Node.hw_model == hw_model)

            if days_active is not None:
                now_us = int(datetime.now(datetime.UTC).timestamp() * 1_000_000)
                cutoff_us = now_us - int(timedelta(days_active).total_seconds() * 1_000_000)
                query = query.where(Node.last_seen_us > cutoff_us)

            # Exclude nodes with missing last_seen_us
            query = query.where(Node.last_seen_us.is_not(None))

            # Order results by long_name in ascending order
            query = query.order_by(Node.short_name.asc())

            # Execute the query and retrieve results
            result = await session.execute(query)
            nodes = result.scalars().all()
            return nodes  # Return the list of nodes

    except Exception:
        logger.exception("error reading DB")
        return []  # Return an empty list in case of failure


async def get_packet_stats(
    period_type: str = "day",
    length: int = 14,
    channel: str | None = None,
    portnum: int | None = None,
    to_node: int | None = None,
    from_node: int | None = None,
):
    now = datetime.now(datetime.UTC)

    if period_type == "hour":
        start_time = now - timedelta(hours=length)
        time_format_sqlite = "%Y-%m-%d %H:00"
        time_format_pg = "YYYY-MM-DD HH24:00"
    elif period_type == "day":
        start_time = now - timedelta(days=length)
        time_format_sqlite = "%Y-%m-%d"
        time_format_pg = "YYYY-MM-DD"
    else:
        raise ValueError("period_type must be 'hour' or 'day'")

    async with database.async_session() as session:
        dialect = session.get_bind().dialect.name
        if dialect == "postgresql":
            period_expr = func.to_char(
                func.to_timestamp(Packet.import_time_us / 1_000_000.0),
                time_format_pg,
            )
        else:
            period_expr = func.strftime(
                time_format_sqlite,
                func.datetime(Packet.import_time_us / 1_000_000, "unixepoch"),
            )

        q = select(
            period_expr.label("period"),
            func.count().label("count"),
        ).where(Packet.import_time_us >= int(start_time.timestamp() * 1_000_000))

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
