# The above classes define Pydantic models for creating and responding with image data, including
# attributes like filename, size, id, upload date, and Kafka status.
from datetime import datetime

from pydantic import BaseModel


class ImageCreateBase(BaseModel):
    filename: str
    size: float


class ImageCreate(ImageCreateBase): ...


class ImageResponse(ImageCreateBase):
    id: int
    upload_date: datetime
    kafka_status: bool

    class Config:
        from_attributes = True
