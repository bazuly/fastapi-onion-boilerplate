"""
    The above code defines dependency injection functions for creating instances of services and
    repositories in a FastAPI application.
    :return: The code snippet defines several dependency functions using FastAPI's `Depends` mechanism
    to retrieve instances of various services and repositories. The functions return instances of
    different classes that are used in the application, such as `ApplicationRepository`,
    `ApplicationService`, `ImageRepository`, and `ImageService`. These instances are created with the
    necessary dependencies injected, such as database sessions, Kafka producers, and logger instances.
"""
import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.service import ApplicationService
from app.broker.producer import KafkaProducer
from app.image_upload.repository.image_repository import ImageRepository
from app.image_upload.service import ImageService
from app.infrastructure.database import get_db_connection
from app.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


async def get_kafka_producer() -> KafkaProducer:
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    return producer


async def get_application_repository(
    db_session: AsyncSession = Depends(get_db_connection),
) -> ApplicationRepository:
    return ApplicationRepository(db_session=db_session)


async def get_application_service(
    application_repository: ApplicationRepository = Depends(get_application_repository),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> ApplicationService:
    return ApplicationService(
        application_repository=application_repository,
        kafka_producer=kafka_producer,
        logger=logger,
    )


async def get_image_upload_repository(
    db_session: AsyncSession = Depends(get_db_connection),
) -> ImageRepository:
    return ImageRepository(db_session=db_session, upload_dir=settings.IMAGE_UPLOAD_DIR)


async def get_image_upload_service(
    image_upload_repository: ImageRepository = Depends(get_image_upload_repository),
    kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> ImageService:
    return ImageService(
        image_repository=image_upload_repository,
        kafka_producer=kafka_producer,
        logger=logger,
    )
