from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi import HTTPException

from app.applications.schema import ApplicationCreateSchema
from app.applications.models import ApplicationModel


class ApplicationRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_application(self, application: ApplicationCreateSchema) -> ApplicationModel:
        query = (
            insert(ApplicationModel)
            .values(
                user_name=application.user_name,
                description=application.description,
            )
            .returning(ApplicationModel)
        )
        async with self.db_session as session:
            result = await session.execute(query)
            await session.commit()
            added_application = result.scalar_one_or_none()
            return added_application

    async def get_all_applications(self, page: int, size: int) -> Sequence[ApplicationModel]:
        offset = (page - 1) * size
        async with self.db_session as session:
            query = select(ApplicationModel).offset(offset).limit(size)
            result = await session.execute(query)
            applications = result.scalars().all()
            if not applications:
                raise HTTPException(status_code=404, detail="No applications found")
        return applications

    async def get_application_by_username(
            self,
            user_name: str,
            page: int,
            size: int
    ) -> Sequence[ApplicationModel]:
        offset = (page - 1) * size
        query = select(ApplicationModel).where(ApplicationModel.user_name == user_name).offset(offset).limit(size)
        async with self.db_session as session:
            result = await session.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="No applications found")
            return result.scalars().all()
