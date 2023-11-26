from fastapi import Depends
from requests import Session

from infrastructure.persistance.base import get_session
from domain.services.expense_service import ExpenseService


def expense_service(
    session: Session = Depends(get_session),
) -> ExpenseService:
    return ExpenseService(session)
