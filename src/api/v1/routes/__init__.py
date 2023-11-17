from fastapi import APIRouter

from .user import user_router

api_router = APIRouter()


api_router.include_router(user_router, prefix="/users", tags=["users"])
