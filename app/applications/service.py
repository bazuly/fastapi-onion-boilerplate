from typing import List, Any
from dataclasses import dataclass

from fastapi import HTTPException

from app.applications.schema import ApplicationCreateSchema, ApplicationSchema
from app.applications.repository.application_repository import ApplicationRepository


@dataclass
class ApplicationService:
    application_repository: ApplicationRepository

    async def create_application(self, body: ApplicationCreateSchema) -> ApplicationSchema:
        created_application = await self.application_repository.create_application(body)
        return ApplicationSchema.model_validate(created_application)

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
        return applications
