from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.image_upload.models import ImageUploadModel
from app.image_upload.repository.image_repository import ImageRepository
from app.image_upload.schema import ImageResponse
from app.broker.producer import KafkaProducer
from settings import settings


@dataclass
class ImageService:
    image_repository: ImageRepository
    kafka_producer: KafkaProducer

    async def upload_image(self, image: Any) -> Any:
        uploaded_image = await self.image_repository.upload_image(image)

        kafka_message = {
            "id": uploaded_image.id,
            "filename": uploaded_image.filename,
            "size": uploaded_image.size,
            "upload_date": uploaded_image.upload_date.isoformat()
        }
        kafka_status = False
        try:
            await self.kafka_producer.produce(
                topic=settings.KAFKA_TOPIC,
                key=str(uploaded_image.id),
                value=kafka_message
            )
            kafka_status = True
        except Exception as e:
            print(f"Error while sending kafka message: {e}")

        return ImageResponse(
            id=uploaded_image.id,
            filename=uploaded_image.filename,
            size=uploaded_image.size,
            upload_date=uploaded_image.upload_date,
            kafka_status=kafka_status
        )

    async def get_image_by_id(self, image_id: int) -> ImageUploadModel:
        image = await self.image_repository.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    async def delete_image_by_id(self, image_id: int) -> dict:
        image = await self.image_repository.delete_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return {
            "msg": f"Image {image_id} deleted successfully"
        }
