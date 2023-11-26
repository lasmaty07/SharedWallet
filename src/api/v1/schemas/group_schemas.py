from datetime import datetime
from pydantic import BaseModel


class GroupRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    name: str
    description: str | None = None


class GroupCreate(BaseModel):
    name: str
    description: str


class GroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
