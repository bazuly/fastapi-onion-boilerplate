from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.service import ApplicationService
from app.broker.producer import KafkaProducer
from app.infrastructure.database import get_db_connection
from settings import settings


async def get_application_repository(db_session: AsyncSession = Depends(get_db_connection)) -> ApplicationRepository:
    return ApplicationRepository(db_session=db_session)


async def get_kafka_producer() -> KafkaProducer:
    producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    return producer


async def get_application_service(
        application_repository: ApplicationRepository = Depends(get_application_repository),
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
) -> ApplicationService:
    return ApplicationService(
        application_repository=application_repository,
        kafka_producer=kafka_producer,
    )
