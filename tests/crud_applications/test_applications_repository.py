import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.applications.repository.application_repository import ApplicationRepository
from app.applications.models import ApplicationModel
from app.applications.schema import ApplicationCreateSchema
from tests.utils.utils import random_lower_string


@pytest.mark.asyncio
async def test_create_application__success(db_session: AsyncSession):
    repository = ApplicationRepository(db_session)

    generated_user_name = random_lower_string()
    generated_description = random_lower_string()

    application_data = ApplicationCreateSchema(user_name=generated_user_name, description=generated_description)
    created_app = await repository.create_application(application_data)

    assert created_app.id is not None
    assert created_app.user_name == generated_user_name
    assert created_app.description == generated_description


@pytest.mark.asyncio
async def test_get_all_applications(db_session: AsyncSession):
    app_1 = ApplicationModel(
        user_name="test_1",
        description="test_descr_1",
    )
    app_2 = ApplicationModel(
        user_name="test_2",
        description="test_descr_2",
    )
    db_session.add_all([app_1, app_2])
    await db_session.commit()

    repository = ApplicationRepository(db_session)
    apps = await repository.get_all_applications(page=1, size=2)
    assert len(apps) == 2
    assert apps[0].user_name == "test_1"


@pytest.mark.asyncio
async def test_get_single_application(db_session: AsyncSession):
    repository = ApplicationRepository(db_session)
    app_1 = ApplicationModel(
        user_name="test_1",
        description="test_descr_1",
    )
    db_session.add(app_1)
    await db_session.commit()

    app = await repository.get_application_by_username("test_1", page=1, size=1)
    assert app is not None


