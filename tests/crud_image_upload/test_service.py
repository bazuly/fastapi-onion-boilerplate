import logging
from unittest.mock import AsyncMock

import pytest

from app.image_upload.service import ImageService
from app.exceptions import KafkaMessageError
from tests.utils.factories import ImageFactory
from tests.utils.utils import kafka_error_detail

logger = logging.getLogger(__name__)

mock_repository = AsyncMock()
mock_kafka = AsyncMock()
user_log_service = AsyncMock()


@pytest.mark.asyncio
async def test_upload_image():
    global mock_repository
    global mock_kafka
    global user_log_service

    data = await ImageFactory.create()
    mock_repository.upload_image.return_value = data

    service = ImageService(mock_repository, mock_kafka,
                           logger, user_log_service)

    result = await service.upload_image(data, data.user_id)
    assert result is not None


@pytest.mark.asyncio
async def test_upload_image__failure():
    global mock_repository
    global mock_kafka
    global user_log_service

    data = await ImageFactory.create()
    mock_repository.upload_image.side_effect = KafkaMessageError(
        details=kafka_error_detail)

    service = ImageService(mock_repository, mock_kafka,
                           logger, user_log_service)

    with pytest.raises(KafkaMessageError):
        await service.upload_image(data, data.user_id)


@pytest.mark.asyncio
async def test_get_image_by_id():
    global mock_repository
    global mock_kafka
    global user_log_service

    data = await ImageFactory.create()
    mock_repository.get_image_by_id.return_value = data

    service = ImageService(mock_repository, mock_kafka,
                           logger, user_log_service)

    result = await service.get_image_by_id(data.id)
    assert result is not None


@pytest.mark.asyncio
async def test_get_image_by_id__failure():
    global mock_repository
    global mock_kafka
    global user_log_service

    data = await ImageFactory.create()
    mock_repository.get_image_by_id.side_effect = KafkaMessageError(
        details=kafka_error_detail)

    service = ImageService(mock_repository, mock_kafka,
                           logger, user_log_service)

    with pytest.raises(KafkaMessageError):
        await service.get_image_by_id(data.id)
