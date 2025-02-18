from dataclasses import dataclass
from datetime import datetime
from typing import List, Any

from fastapi import HTTPException

from app.applications.schema import ApplicationCreateSchema, ApplicationSchema, ApplicationResponseSchema
from app.applications.repository.application_repository import ApplicationRepository
from app.broker.producer import KafkaProducer
from settings import settings


@dataclass
class ApplicationService:
    """
    Service for applications.
    Attributes:
        application_repository: Repository for work with DB
        kafka_producer: Producer for sending messages in Kafka
    """
    application_repository: ApplicationRepository
    kafka_producer: KafkaProducer

    async def create_application(self, body: ApplicationCreateSchema) -> ApplicationResponseSchema:

        created_application = await self.application_repository.create_application(body)

        message = {
            "id": created_application.id,
            "user_name": created_application.user_name,
            "description": created_application.description,
            "created_at": datetime.utcnow().isoformat()
        }

        kafka_status = False
        try:
            await self.kafka_producer.produce(
                topic=settings.KAFKA_TOPIC,
                key=str(created_application.id),
                value=message
            )
            kafka_status = True
        except Exception as e:
            print(f"Error while sending kafka message: {e}")

        return ApplicationResponseSchema(
            id=created_application.id,
            user_name=created_application.user_name,
            description=created_application.description,
            created_at=created_application.created_at,
            kafka_status=kafka_status
        )

    async def get_application_by_user_name(self, user_name: str, page: int, size: int) -> List[ApplicationSchema]:
        applications = await self.application_repository.get_application_by_username(
            user_name=user_name,
            page=page,
            size=size
        )
        if not applications:
            raise HTTPException(status_code=404, detail=f"No applications found for user: {user_name}")

        return [ApplicationSchema.model_validate(app) for app in applications]

    async def get_all_applications(self, page: int, size: int) -> List[ApplicationSchema]:
        applications: Any = await self.application_repository.get_all_applications(page=page, size=size)
        if not applications:
            raise HTTPException(status_code=404, detail=f"No applications found")
        return [ApplicationSchema.model_validate(app) for app in applications]
