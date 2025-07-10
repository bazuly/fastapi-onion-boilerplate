# This class defines an SQLAlchemy model for an application with columns for id, title, description,
# creation timestamp, and user ID.
from datetime import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime, UUID as SQLUUID

from app.infrastructure.database import Base


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=dt.utcnow)
    user_id = Column(SQLUUID, nullable=False)
