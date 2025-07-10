# The above code defines factory classes for creating instances of SQLAlchemy models asynchronously in
# Python.
import uuid
from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat
from sqlalchemy.ext.asyncio import AsyncSession

from factory.declarations import (
    LazyFunction,
    Sequence,
)

from app.applications.models import ApplicationModel
from app.image_upload.models import ImageUploadModel


class AsyncSQLAlchemyModelFactory(SQLAlchemyModelFactory):
    # redifine method create as async method
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        session: AsyncSession = cls._meta.sqlalchemy_session
        instance = model_class(*args, **kwargs)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def create(cls, **kwargs):
        return await super().create(**kwargs)


class BaseFactory(AsyncSQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class ApplicationFactory(BaseFactory):
    """Application factory model"""

    title = Sequence(lambda n: f"application{n}")
    description = FuzzyText()
    created_at = LazyFunction(datetime.now)
    user_id = LazyFunction(uuid.uuid4)

    class Meta:
        model = ApplicationModel


class ImageFactory(BaseFactory):
    """Image factory model."""

    filename = Sequence(lambda n: f"image_{n}.jpg")
    upload_date = LazyFunction(datetime.now)
    size = FuzzyFloat(0.1, 1024.0)
    user_id = LazyFunction(uuid.uuid4)

    class Meta:
        model = ImageUploadModel
