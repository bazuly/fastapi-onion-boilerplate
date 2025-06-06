import json

from aiokafka import AIOKafkaProducer

from app.exceptions import ProducerError


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda x: json.dumps(
                x, indent=4, sort_keys=True, default=str
            ).encode("utf-8"),
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def produce(self, topic: str, key: str, value: dict):
        if not self.producer:
            raise ProducerError("Kafka Producer stopped")

        await self.producer.send_and_wait(topic, value=value, key=key.encode("utf-8"))
        print(f"Message sent to  {topic}: {value}")
