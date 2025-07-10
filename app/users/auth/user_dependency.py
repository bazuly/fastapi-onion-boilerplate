"""
    The above code defines dependencies for retrieving a user database and user manager in a FastAPI
    application.

    :param session: The `session` parameter is an instance of `AsyncSession` from SQLAlchemy's
    `ext.asyncio` module. It is used to interact with the database asynchronously in an asynchronous
    context. In this case, it is being used to create a database connection for user-related operations
    :type session: AsyncSession
"""

from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_connection
from app.users.auth.manager import UserManager
from app.users.auth.models import User


async def get_user_db(
    session: AsyncSession = Depends(get_db_connection),
) -> AsyncGenerator:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
