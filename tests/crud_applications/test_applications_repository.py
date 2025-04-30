import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.schemas import ApplicationCreateSchema
from tests.utils.utils import random_lower_string
from tests.utils.factories import ApplicationFactory


@pytest.mark.asyncio
async def test_create_application__success(db_session: AsyncSession):
    repository = ApplicationRepository(db_session)

    generated_title = random_lower_string()
    generated_description = random_lower_string()
    user_id = uuid.uuid4()

    application_data = ApplicationCreateSchema(title=generated_title, description=generated_description)
    created_app = await repository.create_application(application_data, user_id)

    assert created_app.id is not None
    assert created_app.title == generated_title
    assert created_app.description == generated_description


@pytest.mark.asyncio
async def test_get_all_applications(db_session: AsyncSession):
    app_1 = await ApplicationFactory.create()
    app_2 = await ApplicationFactory.create()

    await db_session.commit()

    repository = ApplicationRepository(db_session)
    apps = await repository.get_all_applications(page=1, size=10)

    assert len(apps) == 2
    assert {app.title for app in apps} == {app_1.title, app_2.title}


@pytest.mark.asyncio
async def test_get_single_application(db_session: AsyncSession):
    repository = ApplicationRepository(db_session)
    app_1 = await ApplicationFactory.create()
    db_session.add(app_1)
    await db_session.commit()

    app = await repository.get_application_by_title(app_1.title)
    assert app is not None
