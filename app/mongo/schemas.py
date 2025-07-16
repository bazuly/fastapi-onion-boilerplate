from datetime import datetime
from typing import Optional
from uuid import UUID


from pydantic import BaseModel


class UserLog(BaseModel):
    user_id: Optional[UUID] = None
    timestamp: datetime
    endpoint: str
