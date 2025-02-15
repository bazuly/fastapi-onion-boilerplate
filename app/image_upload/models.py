from datetime import datetime

from sqlalchemy import DateTime, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class ImageUploadModel(Base):
    __tablename__ = 'image_upload'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    upload_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    size: Mapped[float] = mapped_column(Float, comment="File size in mb")
