from typing import List
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from domain.services.user_service import UserService
from domain.exceptions import EntityNotExists, EntityAlreadyExists
from .exceptions import UserNotFound, UserAlreadyExists
from ..schemas.user_schemas import (
    UserRead,
    UserUpdate,
    UserCreate,
)

# from ..dependencies.auth import authenticate
from ..dependencies.user import user_service


user_router = APIRouter()

# -------------- Users -----------------


@user_router.get(" ", status_code=status.HTTP_200_OK, response_model=List[UserRead])
def get_users(
    page_size: int = 10,
    page: int = 0,
    service: UserService = Depends(user_service),
    # username=Depends(authenticate),
) -> List[UserRead]:
    return service.get_users(page_size, page)


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(user_service),
    # username=Depends(authenticate),
) -> UserRead:
    try:
        return service.get_user(user_id)
    except EntityNotExists:
        raise UserNotFound


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
def create_user(
    user: UserCreate,
    service: UserService = Depends(user_service),
    # username=Depends(authenticate),
) -> None:
    user = UserCreate(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    try:
        service.create_user(user)
    except EntityAlreadyExists:
        raise UserAlreadyExists


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=None,
)
def delete_user(
    user_id: int,
    service: UserService = Depends(user_service),
    # username=Depends(authenticate),
) -> None:
    try:
        service.delete_user(user_id)
    except EntityNotExists:
        raise UserNotFound


@user_router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
def update_user(
    user_id: int,
    user_input: UserUpdate,
    service: UserService = Depends(user_service),
    # username=Depends(authenticate),
) -> UserRead:
    try:
        user: UserRead = service.update_user(
            user_id=user_id,
            user_update=UserUpdate(**user_input.dict()),
        )
        return user.dict()
    except EntityNotExists:
        raise UserNotFound
