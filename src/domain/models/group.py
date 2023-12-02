from datetime import datetime
from dataclasses import dataclass


@dataclass
class Group:
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    name: str
    description: str | None = None
