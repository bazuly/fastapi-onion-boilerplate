import os
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.database import Base
from tests.utils.factories import ApplicationFactory

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
)


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
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False
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
def setup_factories(db_session: AsyncSession):
    ApplicationFactory._meta.sqlalchemy_session = db_session







