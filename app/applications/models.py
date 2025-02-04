from datetime import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime

from app.infrastructure.database import Base


class ApplicationModel(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=dt.utcnow)
