
"""
    The above functions handle the startup and shutdown of a MongoDB client in an asynchronous Python
    application.
    
    :param app: The `app` parameter in the functions `startup_db_client` and `shutdown_db_client` is
    typically an instance of a web application or framework like FastAPI, Flask, or Django. It is used
    to store the MongoDB client connection and database reference so that they can be accessed
    throughout the application
"""
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
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def shutdown_db_client(app):
    try:
        app.mongodb_client.close()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")
