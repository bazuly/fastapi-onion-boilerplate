from datetime import datetime

from sqlalchemy import DateTime, String, Float, Column, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class ImageUploadModel(Base):
    __tablename__ = 'image_upload'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    upload_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    size: Mapped[float] = mapped_column(Float, comment="File size in mb")
    user_id = Column(SQLUUID, nullable=False)

# TODO написать энд ту энд тест авторизация + гет запрос например

# TODO еще сгруппировать материал по подготовке к собесам, который у меня был. Разобрать RestfulAPI, gRPC и метод
# TODO создания api через брокеры сообщений. Плюсы, минусы, принципы, технологии и так далее.

# TODO все ручки сделать, чтобы их мог дергать только аутентифицированный юзер
# TODO и сделать еще патчи для обоих апи
