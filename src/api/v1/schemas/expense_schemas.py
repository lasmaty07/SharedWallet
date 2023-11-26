from datetime import datetime
from pydantic import BaseModel


class ExpenseRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    name: str
    expense_type: str | None = None


class ExpenseCreate(BaseModel):
    name: str
    expense_type: str | None = None


class ExpenseUpdate(BaseModel):
    name: str | None = None
    expense_type: str | None = None
