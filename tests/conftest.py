import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock

from app.main import app
from app.infrastructure.database.database import Base
from app.infrastructure.database.accessor import get_db_session

# don't forget to install aiosqlite
# better to put TEST_DATABASE_URL into .env
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(autouse=True)
def mock_kafka():
    from app.broker import consumer
    consumer.KafkaConsumer = AsyncMock()
    yield


@pytest.fixture
def client():
    from app.main import app
    app.dependency_overrides = {}
    return TestClient(app)


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.close()

    await engine.dispose()


@pytest.fixture
async def override_get_db(db_session):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = _override_get_db
    yield
    del app.dependency_overrides[get_db_session]
