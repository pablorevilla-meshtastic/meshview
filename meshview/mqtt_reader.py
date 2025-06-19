import base64
import asyncio
import random
import aiomqtt
from google.protobuf.message import DecodeError
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from meshtastic.protobuf.mesh_pb2 import Data
from meshtastic.protobuf.mqtt_pb2 import ServiceEnvelope

def decrypt(packet, key):
    if packet.HasField("decoded"):
        return
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
        pass


async def get_topic_envelopes(mqtt_server, mqtt_port, topics, mqtt_user, mqtt_passwd, channel_keys):
    identifier = str(random.getrandbits(16))
    keyring = []
    for k in channel_keys:
        if k == "AQ==":
            k = "1PG7OiApB1nwvP+rz05pAQ=="
        keyring.append(base64.b64decode(k.encode("ascii")))

    while True:
        try:
            async with aiomqtt.Client(
                mqtt_server, port=mqtt_port , username=mqtt_user, password=mqtt_passwd , identifier=identifier,
            ) as client:
                for topic in topics:
                    await client.subscribe(topic)
                async for msg in client.messages:
                    try:
                        envelope = ServiceEnvelope.FromString(msg.payload)
                    except DecodeError:
                        continue
                    for key in keyring:
                        decrypt(envelope.packet, key)
                    if not envelope.packet.decoded:
                        continue
                    yield msg.topic.value, envelope
        except aiomqtt.MqttError as e:
            await asyncio.sleep(1)
