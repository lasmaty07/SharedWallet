from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    name: str
    expense_type: str | None = None
    user_id: int
    group_id: int | None = None
