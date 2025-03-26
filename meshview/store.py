import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import lazyload
from meshview import database
from meshview.models import Packet, PacketSeen, Node, Traceroute
from sqlalchemy import text


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


async def get_packets(node_id=None, portnum=None, since=None, limit=1000, before=None, after=None):
    async with database.async_session() as session:
        q = select(Packet)

        if node_id:
            q = q.where(
                (Packet.from_node_id == node_id) | (Packet.to_node_id == node_id)
            )
        if portnum:
            q = q.where(Packet.portnum == portnum)
        if since:
            q = q.where(Packet.import_time > (datetime.datetime.now() - since))
        if before:
            q = q.where(Packet.import_time < before)
        if after:
            q = q.where(Packet.import_time > after)
        if limit is not None:
            q = q.limit(limit)

        result = await session.execute(q.order_by(Packet.import_time.desc()))
        packets = list(result.scalars())  # Convert to list
        return packets  # Return the list


async def get_packets_from(node_id=None, portnum=None, since=None, limit=500):
    async with database.async_session() as session:
        q = select(Packet)

        if node_id:
            q = q.where(
                Packet.from_node_id == node_id
            )
        if portnum:
            q = q.where(Packet.portnum == portnum)
        if since:
            q = q.where(Packet.import_time > (datetime.datetime.now() - since))
        result = await session.execute(q.limit(limit).order_by(Packet.import_time.desc()))
        return result.scalars()


async def get_packet(packet_id):
    async with database.async_session() as session:
        q = select(Packet).where(Packet.id == packet_id)
        result = await session.execute(q)
        return result.scalar_one_or_none()


async def get_uplinked_packets(node_id, portnum=None):
    async with database.async_session() as session:
        q = select(Packet).join(PacketSeen).where(PacketSeen.node_id == node_id).order_by(Packet.import_time.desc()).limit(500)
        if portnum:
            q = q.where(Packet.portnum == portnum)
        result = await session.execute(q)
        return result.scalars()


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
            (await session.execute(
                    select(Packet.id).where(Packet.from_node_id == node_id).limit(1)
            )).scalar()
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
        result = await session.execute(
                select(Traceroute)
                .join(Packet)
                .where(Traceroute.import_time > (datetime.datetime.now() - since))
                .order_by(Traceroute.import_time)
        )
        return result.scalars()


async def get_mqtt_neighbors(since):
    async with database.async_session() as session:
        result = await session.execute(select(PacketSeen, Packet)
            .join(Packet)
            .where(
                (PacketSeen.hop_limit == PacketSeen.hop_start)
                & (PacketSeen.hop_start != 0)
                & (PacketSeen.import_time > (datetime.datetime.now() - since))
            )
            .options(
                lazyload(Packet.from_node),
                lazyload(Packet.to_node),
            )
        )
        return result


# We count the total amount of packages
# This is to be used by /stats in web.py
async def get_total_packet_count():
    async with database.async_session() as session:
        q = select(func.count(Packet.id))  # Use SQLAlchemy's func to count packets
        result = await session.execute(q)
        return result.scalar()  # Return the total count of packets

# We count the total amount of nodes
async def get_total_node_count():
    async with database.async_session() as session:
        q = select(func.count(Node.id))  # Use SQLAlchemy's func to count nodes
        q = q.where(Node.last_update > datetime.datetime.now() - datetime.timedelta(days=1)) # Look for nodes with nodeinfo updates in the last 24 hours
        result = await session.execute(q)
        return result.scalar()  # Return the total count of nodes

# We count the total amount of seen packets
async def get_total_packet_seen_count():
    async with database.async_session() as session:
        q = select(func.count(PacketSeen.node_id))  # Use SQLAlchemy's func to count nodes
        result = await session.execute(q)
        return result.scalar()  # Return the total count of seen packets


async def get_total_node_count_longfast() -> int:
    try:
        # Open an asynchronous session with the database
        async with database.async_session() as session:
            # Build the query to count nodes where channel == 'LongFast'
            q = select(func.count(Node.id))
            q = q.where(Node.last_update > datetime.datetime.now() - datetime.timedelta( days=1))  # Look for nodes with nodeinfo updates in the last 24 hours
            q = q.where(Node.channel == 'LongFast')  #

            # Execute the query asynchronously and fetch the result
            result = await session.execute(q)

            # Return the scalar value (the count of nodes)
            return result.scalar()
    except Exception as e:
        # Log or handle the exception if needed (optional, replace with logging if necessary)
        print(f"An error occurred: {e}")
        return 0  # Return 0 or an appropriate fallback value in case of an error


async def get_total_node_count_mediumslow() -> int:
    try:
        # Open an asynchronous session with the database
        async with database.async_session() as session:
            # Build the query to count nodes where channel == 'LongFast'
            q = select(func.count(Node.id))
            q = q.where(Node.last_update > datetime.datetime.now() - datetime.timedelta(
                days=1))  # Look for nodes with nodeinfo updates in the last 24 hours
            q = q.where(Node.channel == 'MediumSlow')  #
            # Execute the query asynchronously and fetch the result
            result = await session.execute(q)

            # Return the scalar value (the count of nodes)
            return result.scalar()
    except Exception as e:
        # Log or handle the exception if needed (optional, replace with logging if necessary)
        print(f"An error occurred: {e}")
        return 0  # Return 0 or an appropriate fallback value in case of an error


# Get Nodes for mediumslow only
# p.r.
async def get_nodes_mediumslow():
    async with database.async_session() as session:
        result = await session.execute(
                select(Node)
                .where(
                (Node.channel == "MediumSlow")
                )
        )

        return result.scalars()

async def get_top_traffic_nodes():
    async with database.async_session() as session:
        result = await session.execute(text("""
            SELECT 
                n.node_id,
                n.long_name,
                n.role,
                COUNT(p.id) AS packet_count
            FROM 
                packet p
            JOIN 
                node n
            ON 
                p.from_node_id = n.node_id
            WHERE 
                p.import_time >= DATETIME('now', 'localtime', '-1 day')
            GROUP BY 
                n.long_name, n.role
            ORDER BY 
                packet_count DESC
            LIMIT 100;
        """))

        return result.fetchall()  # Returns a list of tuples

async def get_node_traffic(node_id: int):
    try:
        async with database.async_session() as session:
            result = await session.execute(
                text("""
                    SELECT 
                        node.long_name, packet.portnum, 
                        COUNT(*) AS packet_count
                    FROM packet
                    JOIN node ON packet.from_node_id = node.node_id OR packet.to_node_id = node.node_id
                    WHERE node.node_id = :node_id 
                    AND packet.import_time >= DATETIME('now', 'localtime', '-1 day') 
                    GROUP BY packet.portnum
                    ORDER BY packet_count DESC;
                """), {"node_id": node_id}
            )

            # Map the result to include node.long_name and packet data
            traffic_data = [{
                "long_name": row[0],  # node.long_name
                "portnum": row[1],    # packet.portnum
                "packet_count": row[2]  # COUNT(*) as packet_count
            } for row in result.all()]

            return traffic_data

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error fetching node traffic: {str(e)}")
        return []



async def get_nodes(role=None, channel=None, hw_model=None):
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
            #print(channel)  # Debugging output (consider replacing with logging)

            # Start with a base query selecting all nodes
            query = select(Node)

            # Apply filters based on provided parameters
            if role is not None:
                query = query.where(Node.role == role.upper())  # Ensure role is uppercase
            if channel is not None:
                query = query.where(Node.channel == channel)
            if hw_model is not None:
                query = query.where(Node.hw_model == hw_model)

            # Exclude nodes where last_update is an empty string
            query = query.where(Node.last_update != "")

            # Order results by long_name in ascending order
            query = query.order_by(Node.long_name.asc())

            # Execute the query and retrieve results
            result = await session.execute(query)
            nodes = result.scalars().all()
            return nodes  # Return the list of nodes

    except Exception as e:
        print("error reading DB")  # Consider using logging instead of print
        return []  # Return an empty list in case of failure
