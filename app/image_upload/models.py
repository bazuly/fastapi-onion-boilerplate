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

# TODO написать регистрацию пользователя по jwt например или ouath2 и написать энд ту энд тест.
# TODO еще сгруппировать материал по подготовке к собесам, который у меня был. Разобрать RestfulAPI, gRPC и метод
# TODO создания api через брокеры сообщений. Плюсы, минусы, принципы, технологии и так далее.
# TODO Все schema поменять на schemas S на конце
# TODO все ручки сделать, чтобы их мог дергать только аутентифицированный юзер
