import uuid
from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText
from faker import Faker
from faker.providers import misc
from sqlalchemy.ext.asyncio import AsyncSession

from factory import (
    LazyFunction,
    Sequence,
)

from app.applications.models import ApplicationModel


fake = Faker()
fake.add_provider(misc)


class AsyncSQLAlchemyModelFactory(SQLAlchemyModelFactory):
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
    """ Base factory. """

    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"


class ApplicationFactory(BaseFactory):
    """ Application factory model """

    title = Sequence(lambda n: f"application{n}")
    description = FuzzyText()
    created_at = LazyFunction(datetime.now)
    user_id = LazyFunction(uuid.uuid4)

    class Meta:
        model = ApplicationModel







