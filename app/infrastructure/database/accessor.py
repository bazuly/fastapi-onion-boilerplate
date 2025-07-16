"""
    The function `get_db_session` asynchronously creates and manages a database session with error
    handling using SQLAlchemy in a Python application.
"""
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.exceptions import RepositoryError
from app.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.db_url, future=True, echo=True, pool_pre_ping=True
)

AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise RepositoryError(f"Database error: {str(e)}") from e
        finally:
            await session.close()
