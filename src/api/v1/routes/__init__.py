from fastapi import APIRouter

from .user import user_router
from .group import group_router
from .expense import expense_router

api_router = APIRouter()


api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(group_router, prefix="/groups", tags=["Groups"])
api_router.include_router(expense_router, prefix="/expenses", tags=["Expenses"])