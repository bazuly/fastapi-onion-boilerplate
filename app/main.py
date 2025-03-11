import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from kafka.errors import KafkaError

from app.applications.handlers import router as applications_router
from app.image_upload.handlers import router as image_upload_router
from app.users.auth.handlers import router as users_router
from app.broker.consumer import KafkaConsumer
from app.logger import logger

consumer = KafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    for _ in range(10):
        try:
            await consumer.start()
            break
        except KafkaError as e:
            await asyncio.sleep(2)
            logger.error(
                "Unexpected error during Kafka connection: %s", str(e)
            )
    else:
        raise RuntimeError("Failed to connect to Kafka")

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
