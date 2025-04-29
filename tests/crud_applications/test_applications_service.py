import uuid
import logging
import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.exceptions import HTTPException

from app.applications.schemas import ApplicationCreateSchema, ApplicationResponseSchema
from app.applications.service import ApplicationService
from app.exceptions import KafkaMessageError

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_application__success():
    mock_repository = AsyncMock()
    mock_kafka = AsyncMock()
    user_id = uuid.uuid4()

    mock_repository.create_application.return_value = AsyncMock(
        id=1,
        title="test_title",
        description="Test",
        created_at=datetime.datetime.now(datetime.UTC),
        user_id=user_id,
    )
    service = ApplicationService(mock_repository, mock_kafka, logger)
    app_data = ApplicationCreateSchema(
        title="test_user",
        description="Test",
    )
    result = await service.create_application(app_data, user_id)
    mock_kafka.produce.assert_called_once()
    assert isinstance(result, ApplicationResponseSchema)
    assert result.kafka_status is True


@pytest.mark.asyncio
async def test_create_application__failure():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()
    user_id = uuid.uuid4()

    mock_kafka.produce.side_effect = KafkaMessageError()
    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        title="test_title",
        description="Test",
        created_at=datetime.datetime.now(datetime.UTC),
        user_id=user_id,
    )
    service = ApplicationService(mock_repo, mock_kafka, logger)
    app_data = ApplicationCreateSchema(title="test_title", description="Test")

    result = await service.create_application(app_data, user_id)

    assert result.kafka_status is False


@pytest.mark.asyncio
async def test_get_application_by_title__success():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()
    user_id = uuid.uuid4()

    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        title="test_title",
        description="Test",
        created_at=datetime.datetime.now(datetime.UTC)
    )
    service = ApplicationService(mock_repo, mock_kafka, logger)
    app_data = ApplicationCreateSchema(title="test_title", description="Test")
    created_data = await service.create_application(app_data, user_id)

    get_application_case = await service.get_application_by_title(created_data.title)
    assert get_application_case is not None


@pytest.mark.asyncio
async def test_get_application_by_title__failure():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repo.create_application.return_value = AsyncMock(
        id=1,
        user_name="correct_username",
        description="Test",
        created_at=datetime.datetime.now(datetime.UTC)

    )
    service = ApplicationService(mock_repo, mock_kafka, logger)

    get_application_case = await service.get_application_by_title("incorrect_title")
    assert get_application_case == []


@pytest.mark.asyncio
async def test_get_all_applications__success():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    test_data = [
        AsyncMock(
            id=1,
            title="test_user_1",
            description="Test",
            created_at=datetime.datetime.now(datetime.UTC)
        ),
        AsyncMock(
            id=2,
            title="test_user_2",
            description="Test",
            created_at=datetime.datetime.now(datetime.UTC)
        )
    ]
    mock_repo.get_all_applications.return_value = test_data
    service = ApplicationService(mock_repo, mock_kafka, logger)

    result = await service.get_all_applications(page=1, size=10)

    assert len(result) == 2
    assert result[0].title == "test_user_1"
    assert result[1].title == "test_user_2"


@pytest.mark.asyncio
async def test_get_all_applications__empty():
    mock_repo = AsyncMock()
    mock_kafka = AsyncMock()

    mock_repo.get_all_applications.return_value = []

    service = ApplicationService(mock_repo, mock_kafka, logger)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_all_applications(page=1, size=10)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No applications found"

    mock_repo.get_all_applications.assert_awaited_once_with(page=1, size=10)
