import asyncio
import logging
from contextlib import asynccontextmanager

from aiokafka.errors import KafkaConnectionError
from redis import RedisError

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio.connection import ConnectionPool
from redis import asyncio as redis

from app.applications.handlers import router as applications_router
from app.broker.consumer import KafkaConsumer
from app.image_upload.handlers import router as image_upload_router
from app.users.auth.handlers import router as users_router

logger = logging.getLogger(__name__)
consumer = KafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis lifespan
    retries = 10
    delay = 2

    for attempt in range(retries):
        try:
            logger.info("Attempting to connect to Redis...")
            pool = ConnectionPool.from_url(url="redis://cache:6379/0")
            r = redis.Redis(connection_pool=pool)
            await r.ping()
            FastAPICache.init(
                RedisBackend(r),
                prefix="fastapi-cache:",
                expire=60,
            )
            logger.info("Successfully connected to Redis and initialized cache")
            break
        except RedisError as e:
            logger.error(
                f"Redis connection attempt {attempt + 1}/{retries} failed: {str(e)}"
            )
            if attempt == retries - 1:
                raise RuntimeError(
                    "Failed to connect to Redis after multiple attempts"
                ) from e
            await asyncio.sleep(delay)

    # kafka lifespan
    for attempt in range(retries):
        try:
            await consumer.start()
            break
        except KafkaConnectionError as e:
            print(f"Connection attempt {attempt + 1}/{retries} failed: {str(e)}")
            if attempt == retries - 1:
                raise RuntimeError(
                    "Failed to connect to Kafka after multiple attempts"
                ) from e
            await asyncio.sleep(delay)

    yield

    await consumer.stop()


app = FastAPI(
    lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight.theme": "monokai"}
)

app.include_router(applications_router)
app.include_router(image_upload_router)
app.include_router(users_router)
