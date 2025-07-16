# This code snippet defines a Python class `ApplicationService` that serves as a service layer for
# handling application-related operations. Here's a breakdown of what the code is doing:
import datetime
import logging
from dataclasses import dataclass
from typing import List, Sequence
from uuid import UUID

from fastapi import HTTPException

from app.applications import (
    ApplicationCreateSchema,
    ApplicationSchema,
    ApplicationResponseSchema,
    ApplicationModel
)
from app.applications.repository import ApplicationRepository
from app.mongo import UserLogService
from app.broker.producer import KafkaProducer
from app.exceptions import KafkaMessageError, RecordMongoException
from app.settings import settings

logger = logging.getLogger(__name__)

# TODO сделать так, чтобы если пользователь не авторизован,
# TODO user_id в логах был "no_auth", а если авторизован, то был залоггирован его айди
@dataclass
class ApplicationService:
    application_repository: ApplicationRepository
    kafka_producer: KafkaProducer
    logger: logger
    user_log_service: UserLogService

    async def create_application(
            self,
            body: ApplicationCreateSchema,
            user_id: UUID,
    ) -> ApplicationResponseSchema:
        created_application = await self.application_repository.create_application(
            body, user_id
        )
        try:
            await self.user_log_service.log_endpoint_call(endpoint="create_application", user_id=user_id)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

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
            raise HTTPException(
                status_code=404, detail="Application not found")
        try:
            await self.user_log_service.log_endpoint_call(endpoint="get_application_by_id", user_id=None)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

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
        try:
            await self.user_log_service.log_endpoint_call(endpoint="get_application_by_title", user_id=None)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

        return [ApplicationSchema.model_validate(app) for app in applications]

    async def get_all_applications(
            self, page: int, size: int
    ) -> List[ApplicationSchema]:
        applications: Sequence[
            ApplicationModel
        ] = await self.application_repository.get_all_applications(page=page, size=size)
        if not applications:
            self.logger.error("No applications found")
            raise HTTPException(
                status_code=404, detail="No applications found")
        try:
            await self.user_log_service.log_endpoint_call(endpoint="get_all_applications", user_id=None)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

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

        try:
            await self.user_log_service.log_endpoint_call(endpoint="delete_user_application", user_id=user_id)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

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
        try:
            await self.user_log_service.log_endpoint_call(endpoint="edit_application", user_id=user_id)
        except RecordMongoException as e:
            self.logger.error(
                "Error during data record, MongoDB: {}".format(e))

        return ApplicationSchema.model_validate(updated_application)
