import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.applications.handlers import router as applications_router
from app.image_upload.handlers import router as image_upload_router
from app.users.auth.handlers import router as users_router
from app.broker.consumer import KafkaConsumer

consumer = KafkaConsumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    for _ in range(10):
        try:
            await consumer.start()
            break
        except Exception as e:
            await asyncio.sleep(2)
    else:
        raise RuntimeError("Failed to connect to Kafka")

    yield

    await consumer.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(applications_router)
app.include_router(image_upload_router)
app.include_router(users_router)
