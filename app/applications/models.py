from datetime import datetime as dt
from typing import List

from sqlalchemy import Column, Integer, String, DateTime

from app.infrastructure.database import Base
from app.applications.schema import ApplicationSchema


class ApplicationModel(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=dt.utcnow)

# class PaginatedResponse(Base):
#     items: List[ApplicationSchema]
#     total: int
#     page: int
#     size: int
