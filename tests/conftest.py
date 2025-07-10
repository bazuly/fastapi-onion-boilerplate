"""
    The above code contains fixtures and configurations for testing a FastAPI application with
    SQLAlchemy and Kafka mocking.
"""


import os

import tempfile
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.database import Base
from tests.utils.factories import ApplicationFactory, ImageFactory
from tests.utils.utils import random_lower_string


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
)


@pytest.fixture(autouse=True)
def init_cache():
    """Initialize FastAPICache with in-memory backend for tests"""
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")
    yield
    FastAPICache.reset()


@pytest.fixture(autouse=True)
def mock_kafka():
    from app.broker import consumer

    consumer.KafkaConsumer = AsyncMock()
    yield


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)

    connection = await engine.connect()
    transaction = await connection.begin()

    session_maker = sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )
    session = session_maker()

    try:
        await connection.run_sync(Base.metadata.create_all)
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()
        await engine.dispose()


@pytest.fixture
def client():
    from app.main import app

    app.dependency_overrides = {}
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    monkeypatch.setenv("DB_DRIVE", "postgresql+asyncpg")
    monkeypatch.setenv("DB_HOST", "db-test")
    monkeypatch.setenv("DB_USER", "testuser")
    monkeypatch.setenv("DB_PASSWORD", "testpass")
    monkeypatch.setenv("DB_NAME", "testdb")

    from app.settings import get_settings

    settings = get_settings()
    settings.model_rebuild()


@pytest.fixture(autouse=True)
def application_factory(db_session: AsyncSession):
    ApplicationFactory._meta.sqlalchemy_session = db_session


@pytest.fixture(autouse=True)
def image_factory(db_session: AsyncSession):
    ImageFactory._meta.sqlalchemy_session = db_session


@pytest.fixture
def mock_file():
    class MockFile:
        filename = random_lower_string() + ".jpg"

        async def read(self):
            return b"fake content"

    return MockFile()


@pytest.fixture
def tmp_upload_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir
