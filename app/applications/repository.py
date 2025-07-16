# The `ApplicationRepository` class provides methods for interacting with application data in a
# database, including creating, retrieving, updating, and deleting applications, with caching
# functionality implemented for certain operations.
from typing import Sequence
import logging
from uuid import UUID

from fastapi import HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications import ApplicationModel, ApplicationCreateSchema

logger = logging.getLogger(__name__)


class ApplicationRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = logger

    async def create_application(
        self, application: ApplicationCreateSchema, user_id: UUID
    ) -> ApplicationModel:
        query = (
            insert(ApplicationModel)
            .values(
                title=application.title,
                description=application.description,
                user_id=user_id,
            )
            .returning(ApplicationModel)
        )
        async with self.db_session as session:
            result = await session.execute(query)
            await session.commit()
            added_application = result.scalar_one_or_none()
            self.logger.info("Application added by user: %s", user_id)
            return added_application

    @staticmethod
    @cache(expire=120)
    async def get_user_application(
        application_id: int, user_id: UUID, session: AsyncSession
    ) -> ApplicationModel:
        query = select(ApplicationModel).where(
            ApplicationModel.id == application_id, ApplicationModel.user_id == user_id
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_application_by_id(self, application_id: int) -> ApplicationModel:
        query = select(ApplicationModel).where(
            ApplicationModel.id == application_id)
        async with self.db_session as session:
            application: ApplicationModel = (
                await session.execute(query)
            ).scalar_one_or_none()
            if not application:
                self.logger.warning("Application does not exist")
                raise HTTPException(
                    status_code=404, detail="Application not found")
            self.logger.info("Application found by id: %s", application_id)
        return application

    @cache(expire=120)
    async def get_all_applications(
        self,
        page: int,
        size: int,
    ) -> Sequence[ApplicationModel]:
        offset = (page - 1) * size
        async with self.db_session as session:
            query = select(ApplicationModel).offset(offset).limit(size)
            result = await session.execute(query)
            applications = result.scalars().all()
            if not applications:
                self.logger.warning("No applications found")
                raise HTTPException(
                    status_code=404, detail="No applications found")

        return applications

    @cache(expire=120)
    async def get_application_by_title(
        self,
        title: str,
    ) -> Sequence[ApplicationModel]:
        query = select(ApplicationModel).where(ApplicationModel.title == title)
        async with self.db_session as session:
            result = await session.execute(query)
            if not result:
                self.logger.warning(
                    "No application found with title: %s", title)
                raise HTTPException(
                    status_code=404, detail="No applications found")
            self.logger.info("Application found with title: %s", title)
            return result.scalars().all()

    async def delete_user_application(self, application_id: int, user_id: UUID) -> dict:
        query = select(ApplicationModel).where(
            ApplicationModel.id == application_id, ApplicationModel.user_id == user_id
        )

        async with self.db_session as session:
            result = await session.execute(query)
            application = result.scalar_one_or_none()

            if not application:
                self.logger.error(
                    "Application delete attempt failed",
                    extra={
                        "application_id": application_id,
                        "user_id": str(user_id),
                        "reason": "not_found_or_access_denied",
                    },
                )
                raise HTTPException(
                    status_code=404, detail="Application not found")

            delete_query = delete(ApplicationModel).where(
                ApplicationModel.id == application_id
            )
            self.logger.info(
                "Application deleted",
                extra={
                    "application_id": application_id,
                    "user_id": str(user_id),
                },
            )
            await session.execute(delete_query)
            await session.commit()

        return {"status": "success", "message": "Application deleted"}

    async def edit_application_info(
        self,
        application_id: int,
        user_id: UUID,
        new_title: str | None = None,
        new_description: str | None = None,
    ) -> ApplicationModel:
        async with self.db_session as session:
            application = await self.get_user_application(
                application_id, user_id, session
            )

            if not application:
                self.logger.warning(
                    "Application edit attempt failed",
                    extra={
                        "application_id": application_id,
                        "user_id": str(user_id),
                        "reason": "not_found_or_access_denied",
                    },
                )
                raise HTTPException(
                    status_code=404, detail="Application not found or access denied"
                )

            update_data = {}
            if new_title is not None:
                update_data["title"] = new_title
            if new_description is not None:
                update_data["description"] = new_description

            if update_data:
                await session.execute(
                    update(ApplicationModel)
                    .where(ApplicationModel.id == application_id)
                    .values(**update_data)
                )
                self.logger.info(
                    "Application updated",
                    extra={
                        "application_id": application_id,
                        "user_id": str(user_id),
                        "update_data": update_data,
                    },
                )
                await session.commit()
                await session.refresh(application)

            return application
