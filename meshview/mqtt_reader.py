import asyncio
import base64
import logging
import random
import time

import aiomqtt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from google.protobuf.message import DecodeError

from meshtastic.protobuf.mesh_pb2 import Data
from meshtastic.protobuf.mqtt_pb2 import ServiceEnvelope
from meshview.config import CONFIG

PRIMARY_KEY = base64.b64decode("1PG7OiApB1nwvP+rz05pAQ==")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d [pid:%(process)d] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def _parse_skip_node_ids():
    mqtt_config = CONFIG.get("mqtt", {})
    raw_value = mqtt_config.get("skip_node_ids", "")
    if not raw_value:
        return set()

    if isinstance(raw_value, str):
        raw_value = raw_value.strip()
        if not raw_value:
            return set()
        values = [v.strip() for v in raw_value.split(",") if v.strip()]
    else:
        values = [raw_value]

    skip_ids = set()
    for value in values:
        try:
            skip_ids.add(int(value, 0))
        except (TypeError, ValueError):
            logger.warning("Invalid node id in mqtt.skip_node_ids: %s", value)
    return skip_ids


def _strip_quotes(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _parse_secondary_keys():
    mqtt_config = CONFIG.get("mqtt", {})
    raw_value = mqtt_config.get("secondary_keys", "")
    if not raw_value:
        return []

    if isinstance(raw_value, str):
        raw_value = raw_value.strip()
        if not raw_value:
            return []
        values = [v.strip() for v in raw_value.split(",") if v.strip()]
    else:
        values = [raw_value]

    keys = []
    for value in values:
        try:
            cleaned = _strip_quotes(str(value).strip())
            if cleaned:
                keys.append(base64.b64decode(cleaned))
        except (TypeError, ValueError):
            logger.warning("Invalid base64 key in mqtt.secondary_keys: %s", value)
    return keys


SKIP_NODE_IDS = _parse_skip_node_ids()
SECONDARY_KEYS = _parse_secondary_keys()

logger.info("Primary key: %s", PRIMARY_KEY)
if SECONDARY_KEYS:
    logger.info("Secondary keys: %s", SECONDARY_KEYS)
else:
    logger.info("Secondary keys: []")

# Thank you to "Robert Grizzell" for the decryption code!
# https://github.com/rgrizzell
def decrypt(packet, key):
    if packet.HasField("decoded"):
        return True
    packet_id = packet.id.to_bytes(8, "little")
    from_node_id = getattr(packet, "from").to_bytes(8, "little")
    nonce = packet_id + from_node_id

    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    raw_proto = decryptor.update(packet.encrypted) + decryptor.finalize()
    try:
        data = Data()
        data.ParseFromString(raw_proto)
        packet.decoded.CopyFrom(data)
    except DecodeError:
        return False
    return True


async def get_topic_envelopes(mqtt_server, mqtt_port, topics, mqtt_user, mqtt_passwd):
    identifier = str(random.getrandbits(16))
    keyring = [PRIMARY_KEY, *SECONDARY_KEYS]
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

                    for key in keyring:
                        if decrypt(envelope.packet, key):
                            break
                    if not envelope.packet.decoded:
                        continue

                    # Skip packets from configured node IDs
                    if getattr(envelope.packet, "from", None) in SKIP_NODE_IDS:
                        continue

                    msg_count += 1
                    # FIXME: make this interval configurable or time based
                    if (
                        msg_count % 10000 == 0
                    ):  # Log notice every 10000 messages (approx every hour at 3/sec)
                        elapsed_time = time.time() - start_time
                        msg_rate = msg_count / elapsed_time if elapsed_time > 0 else 0
                        logger.info(
                            f"Processed {msg_count} messages so far... ({msg_rate:.2f} msg/sec)"
                        )

                    yield msg.topic.value, envelope

        except aiomqtt.MqttError as e:
            logger.error(f"MQTT error: {e}, reconnecting in 1s...")
            await asyncio.sleep(1)
