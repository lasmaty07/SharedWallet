from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.exceptions import EntityAlreadyExists
from infrastructure.persistance.models.expense import Expense
from api.v1.schemas.expense_schemas import (
    ExpenseCreate,
    ExpenseRead,
)


class ExpenseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def to_domain(expense: Expense) -> ExpenseRead:
        return ExpenseRead(
            id=expense.id,
            created_at=expense.created_at,
            updated_at=expense.updated_at,
            deleted_at=expense.deleted_at,
            name=expense.name,
            expense_type=expense.expense_type,
        )

    @staticmethod
    def to_persistance(expense: ExpenseCreate) -> Expense:
        return Expense(name=expense.name, expense_type=expense.expense_type)

    def add(self, expense: Expense) -> ExpenseRead:
        self.session.add(expense)
        try:
            self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExists

        self.session.refresh(expense)
        return expense

    def get_all(self, page_size: int, page: int):
        expenses = self.session.execute(
            select(Expense)
            .where(Expense.deleted_at == None)
            .limit(page_size)
            .offset(page_size * page)
        ).all()
        return [expense[0] for expense in expenses]

    def get_without_map(self, expense_id: int) -> Expense:
        expense = self.session.execute(
            select(Expense).where(
                Expense.id == expense_id,
                Expense.deleted_at == None,
            )
        ).first()
        if expense:
            return expense[0]

    def get(self, expense_id: int) -> ExpenseRead | None:
        expense = self.session.execute(
            select(Expense).where(
                Expense.id == expense_id,
                Expense.deleted_at == None,
            )
        ).first()
        if expense:
            return self.to_domain(expense[0])

    def update(self, expense: Expense) -> ExpenseRead:
        self.session.commit()
        self.session.refresh(expense)
        return self.to_domain(expense)

    def delete(self, expense_id: int):
        expense = self.session.execute(
            select(Expense).where(Expense.id == expense_id)
        ).first()
        if expense:
            expense[0].deleted_at = datetime.now()
            self.session.commit()
            return True
        return False
