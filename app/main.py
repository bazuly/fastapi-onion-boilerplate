import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.applications.handlers import router as applications_router
from app.broker.consumer import KafkaConsumer
from app.exceptions import KafkaLifeSpawnError
from app.image_upload.handlers import router as image_upload_router
from app.users.auth.handlers import router as users_router

consumer = KafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    retries = 10
    delay = 2

    for attempt in range(retries):
        try:
            await consumer.start()
            break
        except KafkaLifeSpawnError as e:
            if attempt == retries - 1:
                raise RuntimeError("Failed to connect to Kafka after multiple attempts") from e
            await asyncio.sleep(delay)

    yield

    await consumer.stop()


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai"
    }
)

app.include_router(applications_router)
app.include_router(image_upload_router)
app.include_router(users_router)
