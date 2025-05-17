import uuid
import os

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ImageNotFoundError
from app.image_upload.models import ImageUploadModel
from app.image_upload.repository.image_repository import ImageRepository
from tests.conftest import tmp_upload_dir
from tests.utils.factories import ImageFactory


@pytest.mark.asyncio
class TestImageRepository:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, tmp_upload_dir: str, db_session: AsyncSession):
        self.repo = ImageRepository(db_session, tmp_upload_dir)
        ImageFactory._meta.sqlalchemy_session = db_session
        self.user_id = uuid.uuid4()

    async def test_upload_image__success(self, mock_file, db_session, tmp_upload_dir) -> None:
        result = await self.repo.upload_image(mock_file, self.user_id)

        assert isinstance(result, ImageUploadModel)
        assert os.path.exists(os.path.join(self.repo.upload_dir, mock_file.filename))

    async def test_get_image__success(self, mock_file, db_session) -> None:
        image = await self.repo.upload_image(mock_file, self.user_id)

        result = await self.repo.get_image_by_id(image.id)
        assert result.id == image.id
        assert result.filename == image.filename

    async def test_get_image_not_found(self) -> None | ImageNotFoundError:
        try:
            await self.repo.get_image_by_id(999)
        except:
            raise ImageNotFoundError(999)

    async def test_delete_image__success(self, mock_file, db_session, tmp_upload_dir) -> None:
        image = await self.repo.upload_image(mock_file, self.user_id)
        file_path = os.path.join(self.repo.upload_dir, image.filename)
        open(file_path, "w").close()

        await self.repo.delete_image_by_id(image.id, self.user_id)
        assert not os.path.exists(file_path)
