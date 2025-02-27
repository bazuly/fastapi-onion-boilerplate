from datetime import datetime as dt

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: dt

    class Config:
        from_attributes = True


class ApplicationCreateSchema(BaseModel):
    title: str
    description: str | None


class ApplicationResponseSchema(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: dt
    kafka_status: bool

    class Config:
        from_attributes = True
