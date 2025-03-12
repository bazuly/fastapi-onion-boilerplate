from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_connection
from app.users.auth.manager import UserManager
from app.users.auth.models import User


async def get_user_db(session: AsyncSession = Depends(get_db_connection)) -> SQLAlchemyUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
