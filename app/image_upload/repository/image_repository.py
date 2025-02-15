import os
from typing import Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.image_upload.models import ImageUploadModel


class ImageRepository:
    def __init__(self, db_session: AsyncSession, upload_dir: str):
        self.db_session = db_session
        self.upload_dir = upload_dir

    async def upload_image(self, image: Any) -> ImageUploadModel:
        os.makedirs(self.upload_dir, exist_ok=True)

        file_path = os.path.join(self.upload_dir, image.filename)
        content = await image.read()

        with open(file_path, "wb") as f:
            f.write(content)

        image = ImageUploadModel(
            filename=image.filename,
            upload_date=datetime.utcnow(),
            size=len(content) / 1024 / 1024,
        )
        self.db_session.add(image)
        await self.db_session.commit()
        await self.db_session.refresh(image)
        return image

    async def get_image_by_id(self, image_id: int) -> ImageUploadModel | None:
        result = await self.db_session.execute(
            select(ImageUploadModel).where(ImageUploadModel.id == image_id)
        )
        return result.scalar_one_or_none()

    async def delete_image_by_id(self, image_id: int) -> None:
        image = await self.db_session.execute(
            select(ImageUploadModel).where(ImageUploadModel.id == image_id)
        )
        if not image:
            raise ValueError(f"Image with id {image_id} does not exist")

        image = image.scalar_one_or_none()

        await self.db_session.delete(image)
        await self.db_session.commit()
