import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.schemas import ApplicationCreateSchema
from tests.utils.factories import ApplicationFactory


@pytest.mark.asyncio
async def test_create_application__success(db_session: AsyncSession):
    repository = ApplicationRepository(db_session)

    raw_data = await ApplicationFactory.create()
    title = raw_data.title
    description = raw_data.description
    user_id = raw_data.user_id

    application_data = ApplicationCreateSchema(title=title, description=description)
    created_app = await repository.create_application(application_data, user_id)

    assert created_app.id is not None
    assert created_app.title == raw_data.title
    assert created_app.description == raw_data.description


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
