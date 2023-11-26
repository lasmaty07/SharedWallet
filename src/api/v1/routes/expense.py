from typing import List
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from domain.services.expense_service import ExpenseService
from domain.exceptions import EntityNotExists, EntityAlreadyExists
from .exceptions import ExpenseNotFound, ExpenseAlreadyExists
from ..schemas.expense_schemas import (
    ExpenseRead,
    ExpenseUpdate,
    ExpenseCreate,
)

# from ..dependencies.auth import authenticate
from ..dependencies.expense import expense_service


expense_router = APIRouter()

# -------------- Expenses -----------------


@expense_router.get(
    " ", status_code=status.HTTP_200_OK, response_model=List[ExpenseRead]
)
def get_expenses(
    page_size: int = 10,
    page: int = 0,
    service: ExpenseService = Depends(expense_service),
    # username=Depends(authenticate),
) -> List[ExpenseRead]:
    return service.get_expenses(page_size, page)


@expense_router.get(
    "/{expense_id}", status_code=status.HTTP_200_OK, response_model=ExpenseRead
)
def get_expense(
    expense_id: int,
    service: ExpenseService = Depends(expense_service),
    # username=Depends(authenticate),
) -> ExpenseRead:
    try:
        return service.get_expense(expense_id)
    except EntityNotExists:
        raise ExpenseNotFound


@expense_router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
def create_expense(
    expense: ExpenseCreate,
    service: ExpenseService = Depends(expense_service),
    # username=Depends(authenticate),
) -> None:
    expense = ExpenseCreate(
        name=expense.name,
        description=expense.description,
    )
    try:
        service.create_expense(expense)
    except EntityAlreadyExists:
        raise ExpenseAlreadyExists


@expense_router.delete(
    "/{expense_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=None,
)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(expense_service),
    # username=Depends(authenticate),
) -> None:
    try:
        service.delete_expense(expense_id)
    except EntityNotExists:
        raise ExpenseNotFound


@expense_router.patch(
    "/{expense_id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseRead,
)
def update_expense(
    expense_id: int,
    expense_input: ExpenseUpdate,
    service: ExpenseService = Depends(expense_service),
    # username=Depends(authenticate),
) -> ExpenseRead:
    try:
        expense: ExpenseRead = service.update_expense(
            expense_id=expense_id,
            expense_update=ExpenseUpdate(**expense_input.dict()),
        )
        return expense.dict()
    except EntityNotExists:
        raise ExpenseNotFound
