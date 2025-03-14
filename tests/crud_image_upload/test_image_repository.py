import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.image_upload.repository.image_repository import ImageRepository


@pytest.mark.asyncio
async def test_upload_image_repository__success(db_session: AsyncSession) -> None:
    upload_dir = "test_uploads/test_image/"
    repository = ImageRepository(db_session, upload_dir)

    os.makedirs(upload_dir, exist_ok=True)
