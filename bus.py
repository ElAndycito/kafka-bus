import json
from confluent_kafka import Producer, Consumer

BOOTSTRAP = "localhost:9092"
_producer = None


def publish(topic: str, mensaje: dict, key: str | None = None):
    global _producer
    if _producer is None:
        _producer = Producer({"bootstrap.servers": BOOTSTRAP})
    _producer.produce(topic, key=key, value=json.dumps(mensaje).encode("utf-8"))
    _producer.flush()


def consume(topic: str, group_id: str):
    c = Consumer({
        "bootstrap.servers": BOOTSTRAP,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    })
    c.subscribe([topic])
    try:
        while True:
            m = c.poll(1.0)
            if m is None:
                continue
            if m.error():
                print("Error Kafka:", m.error())
                continue
            yield json.loads(m.value().decode("utf-8"))
    finally:
        c.close()