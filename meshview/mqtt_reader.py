import base64
import asyncio
import random
import time
import aiomqtt
import logging
from google.protobuf.message import DecodeError
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from meshtastic.protobuf.mqtt_pb2 import ServiceEnvelope

KEY = base64.b64decode("1PG7OiApB1nwvP+rz05pAQ==")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d [pid:%(process)d] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def decrypt(packet):
    if packet.HasField("decoded"):
        return
    packet_id = packet.id.to_bytes(8, "little")
    from_node_id = getattr(packet, "from").to_bytes(8, "little")
    nonce = packet_id + from_node_id

    cipher = Cipher(algorithms.AES(KEY), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    raw_proto = decryptor.update(packet.encrypted) + decryptor.finalize()
    try:
        packet.decoded.ParseFromString(raw_proto)
    except DecodeError:
        pass


async def get_topic_envelopes(mqtt_server, mqtt_port, topics, mqtt_user, mqtt_passwd):
    identifier = str(random.getrandbits(16))
    msg_count = 0
    start_time = None
    while True:
        try:
            async with aiomqtt.Client(
                mqtt_server,
                port=mqtt_port,
                username=mqtt_user,
                password=mqtt_passwd,
                identifier=identifier,
            ) as client:

                logger.info(f"Connected to MQTT broker at {mqtt_server}:{mqtt_port}")
                for topic in topics:
                    logger.info(f"Subscribing to: {topic}")
                    await client.subscribe(topic)

                # Reset start time when connected
                if start_time is None:
                    start_time = time.time()

                async for msg in client.messages:
                    try:
                        envelope = ServiceEnvelope.FromString(msg.payload)
                    except DecodeError:
                        continue

                    decrypt(envelope.packet)
                    # print(envelope.packet.decoded)
                    if not envelope.packet.decoded:
                        continue

                    # Skip packets from specific node
                    # FIXME: make this configurable as a list of node IDs to skip
                    if getattr(envelope.packet, "from", None) == 2144342101:
                        continue

                    msg_count += 1
                    # FIXME: make this interval configurable or time based
                    if msg_count % 10000 == 0:  # Log notice every 10000 messages (approx every hour at 3/sec)
                        elapsed_time = time.time() - start_time
                        msg_rate = msg_count / elapsed_time if elapsed_time > 0 else 0
                        logger.info(f"Processed {msg_count} messages so far... ({msg_rate:.2f} msg/sec)")

                    yield msg.topic.value, envelope

        except aiomqtt.MqttError as e:
            logger.error(f"MQTT error: {e}, reconnecting in 1s...")
            await asyncio.sleep(1)
