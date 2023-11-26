from typing import List
from sqlalchemy.orm import Session

from api.v1.schemas.expense_schemas import (
    ExpenseRead,
    ExpenseCreate,
    ExpenseUpdate,
)
from domain.exceptions import EntityNotExists
from src.infrastructure.persistance.models.expense import Expense
from infrastructure.persistance.repositories.expense_repository import (
    ExpenseRepository,
)


class ExpenseService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = ExpenseRepository(self.session)

    def get_expenses(self, page_size: int, page: int) -> List[ExpenseCreate]:
        return [
            self.repository.to_domain(expense)
            for expense in self.repository.get_all(page_size, page)
        ]

    def get_expense(self, expense_id: int) -> ExpenseRead:
        instance: Expense = self.repository.get(expense_id)
        if not instance:
            raise EntityNotExists
        expense_read = self.repository.to_domain(instance)
        return expense_read

    def create_expense(
        self,
        expense_create: ExpenseCreate,
    ) -> ExpenseRead:
        expense = self.repository.to_persistance(expense_create)
        expense_read = self.repository.add(expense)
        return expense_read

    def update_expense(
        self,
        expense_id: int,
        expense_update: ExpenseUpdate,
    ) -> ExpenseRead:
        expense: Expense = self.repository.get_without_map(expense_id)
        if not expense:
            raise EntityNotExists
        for k, v in expense_update.dict(exclude_unset=True).items():
            if v:
                setattr(expense, k, v)
        expense_read = self.repository.update(expense)
        return expense_read

    def delete_expense(self, expense_id: int):
        return self.repository.delete(expense_id)
