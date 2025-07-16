import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.settings import settings

logger = logging.getLogger(__name__)


async def startup_db_client(app):
    try:
        app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        # db connection
        app.mongodb = app.mongodb_client["user_logs"]

        logger.info("MongoDB connected successfully")
        print("MongoDB connected successfully")  # TODO remove later
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def shutdown_db_client(app):
    try:
        app.mongodb_client.close()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")


# TODO Настроить структурированное логирование
