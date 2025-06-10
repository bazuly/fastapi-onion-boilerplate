import datetime
import logging
from dataclasses import dataclass
from typing import List, Sequence
from uuid import UUID

from fastapi import HTTPException

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.schemas import (
    ApplicationCreateSchema,
    ApplicationSchema,
    ApplicationResponseSchema,
)
from app.applications.models import ApplicationModel
from app.broker.producer import KafkaProducer
from app.exceptions import KafkaMessageError
from app.settings import settings

logger = logging.getLogger(__name__)


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
    logger: logger

    async def create_application(
        self,
        body: ApplicationCreateSchema,
        user_id: UUID,
    ) -> ApplicationResponseSchema:
        created_application = await self.application_repository.create_application(
            body, user_id
        )

        message = {
            "id": created_application.id,
            "title": created_application.title,
            "description": created_application.description,
            "created_at": datetime.datetime.now(datetime.UTC),
            "user_id": str(user_id),
        }

        kafka_status = False
        try:
            await self.kafka_producer.produce(
                topic=settings.KAFKA_TOPIC,
                key=str(created_application.id),
                value=message,
            )
            kafka_status = True
        except KafkaMessageError as e:
            self.logger.error(
                "Error while sending message to Kafka: {}".format(e),
            )

        return ApplicationResponseSchema(
            id=created_application.id,
            title=created_application.title,
            description=created_application.description,
            created_at=created_application.created_at,
            kafka_status=kafka_status,
        )

    async def get_application_by_id(self, application_id: int) -> ApplicationSchema:
        application = await self.application_repository.get_application_by_id(
            application_id
        )
        if not application:
            self.logger.error(
                "Application with application id: %s not found", application_id
            )
            raise HTTPException(status_code=404, detail="Application not found")
        return ApplicationSchema.model_validate(application)

    async def get_application_by_title(self, title: str) -> List[ApplicationSchema]:
        applications = await self.application_repository.get_application_by_title(
            title=title,
        )
        if not applications:
            self.logger.warning("Application with title: %s not found", title)
            raise HTTPException(
                status_code=404, detail=f"No applications found titled {title}"
            )

        return [ApplicationSchema.model_validate(app) for app in applications]

    async def get_all_applications(
        self, page: int, size: int
    ) -> List[ApplicationSchema]:
        applications: Sequence[
            ApplicationModel
        ] = await self.application_repository.get_all_applications(page=page, size=size)
        if not applications:
            self.logger.error("No applications found")
            raise HTTPException(status_code=404, detail="No applications found")
        return [ApplicationSchema.model_validate(app) for app in applications]

    async def delete_user_application(self, application_id: int, user_id: UUID):
        try:
            return await self.application_repository.delete_user_application(
                application_id=application_id, user_id=user_id
            )

        except HTTPException as e:
            self.logger.error(
                "Error while deleting user application:", extra={"error_detail": str(e)}
            )
            return None

    async def edit_application(
        self,
        application_id: int,
        user_id: UUID,
        new_title: str | None = None,
        new_description: str | None = None,
    ) -> ApplicationSchema:
        updated_application = await self.application_repository.edit_application_info(
            application_id=application_id,
            user_id=user_id,
            new_title=new_title,
            new_description=new_description,
        )
        if not updated_application:
            raise HTTPException(
                status_code=404, detail=f"No application found for user: {user_id}"
            )
        return ApplicationSchema.model_validate(updated_application)
