from datetime import datetime

import pytest
from unittest.mock import AsyncMock
from app.applications.service import ApplicationService
from app.applications.schema import ApplicationCreateSchema, ApplicationResponseSchema
from fastapi.exceptions import HTTPException


@pytest.mark.asyncio
async def test_create_application__success():
    mock_repository = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repository.create_application.return_value = AsyncMock(
        id=1,
        user_name="test_user",
        description="Test",
        created_at=datetime.utcnow()
    )
    service = ApplicationService(mock_repository, mock_kafka)
    app_data = ApplicationCreateSchema(
        user_name="test_user",
        description="Test",
    )
    result = await service.create_application(app_data)
    mock_kafka.produce.assert_called_once()
    assert isinstance(result, ApplicationResponseSchema)
    assert result.kafka_status is True


@pytest.mark.asyncio
async def test_create_application__failure():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_kafka.produce.side_effect = Exception("Kafka error")
    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        user_name="test_user",
        description="Test",
        created_at=datetime.utcnow()
    )
    service = ApplicationService(mock_repo, mock_kafka)
    app_data = ApplicationCreateSchema(user_name="test_user", description="Test")

    result = await service.create_application(app_data)

    assert result.kafka_status is False


@pytest.mark.asyncio
async def test_get_application_by_username__success():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        user_name="test_user",
        description="Test",
        created_at=datetime.utcnow()
    )
    service = ApplicationService(mock_repo, mock_kafka)
    app_data = ApplicationCreateSchema(user_name="test_user", description="Test")
    created_data = await service.create_application(app_data)

    get_application_case = await service.get_application_by_user_name(created_data.user_name, page=1, size=1)
    assert get_application_case is not None


@pytest.mark.asyncio
async def test_get_application_by_username__failure():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        user_name="correct_username",
        description="Test",
        created_at=datetime.utcnow()
    )
    service = ApplicationService(mock_repo, mock_kafka)

    get_application_case = await service.get_application_by_user_name("incorrect_username", page=1, size=1)
    assert get_application_case == []


@pytest.mark.asyncio
async def test_get_all_applications__success():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    test_data = [
        AsyncMock(
            id=1,
            user_name="test_user_1",
            description="Test",
            created_at=datetime.utcnow()
        ),
        AsyncMock(
            id=2,
            user_name="test_user_2",
            description="Test",
            created_at=datetime.utcnow()
        )
    ]
    mock_repo.get_all_applications.return_value = test_data
    service = ApplicationService(mock_repo, mock_kafka)

    result = await service.get_all_applications(page=1, size=10)

    assert len(result) == 2
    assert result[0].user_name == "test_user_1"
    assert result[1].user_name == "test_user_2"


@pytest.mark.asyncio
async def test_get_all_applications__empty():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repo.get_all_applications.return_value = []

    service = ApplicationService(mock_repo, mock_kafka)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_all_applications(page=1, size=10)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No applications found"

    mock_repo.get_all_applications.assert_awaited_once_with(page=1, size=10)
