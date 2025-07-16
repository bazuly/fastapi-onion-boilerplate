# This class defines a Kafka consumer in Python using aiokafka library for consuming messages from a
# Kafka topic.
import asyncio
import json

from aiokafka import AIOKafkaConsumer

from app.exceptions import ConsumerError
from app.settings import settings


class KafkaConsumer:
    def __init__(self):
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
            value_deserializer=lambda v: json.loads(v.decode()),
        )
        await self.consumer.start()
        asyncio.create_task(self.consume_messages())

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                print("\n" + "=" * 50)
                print("Received Kafka message:")
                print(f"Topic: {msg.topic}")
                print(f"Key: {msg.key.decode()}")
                print(f"Value: {msg.value}")
                print("=" * 50 + "\n")
        except ConsumerError as e:
            print(f"Consumer error: {str(e)}")
            await asyncio.sleep(2)
