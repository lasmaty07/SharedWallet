from typing import List
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from domain.services.group_service import GroupService
from domain.exceptions import EntityNotExists, EntityAlreadyExists
from .exceptions import GroupNotFound, GroupAlreadyExists
from ..schemas.group_schemas import (
    GroupRead,
    GroupUpdate,
    GroupCreate,
)

# from ..dependencies.auth import authenticate
from ..dependencies.group import group_service


group_router = APIRouter()

# -------------- Groups -----------------


@group_router.get(
    " ", status_code=status.HTTP_200_OK, response_model=List[GroupRead]
)
def get_groups(
    page_size: int = 10,
    page: int = 0,
    service: GroupService = Depends(group_service),
    # username=Depends(authenticate),
) -> List[GroupRead]:
    return service.get_groups(page_size, page)


@group_router.get(
    "/{group_id}", status_code=status.HTTP_200_OK, response_model=GroupRead
)
def get_group(
    group_id: int,
    service: GroupService = Depends(group_service),
    # username=Depends(authenticate),
) -> GroupRead:
    try:
        return service.get_group(group_id)
    except EntityNotExists:
        raise GroupNotFound


@group_router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
def create_group(
    group: GroupCreate,
    service: GroupService = Depends(group_service),
    # username=Depends(authenticate),
) -> None:
    group = GroupCreate(
        name=group.name,
        description=group.description,
    )
    try:
        service.create_group(group)
    except EntityAlreadyExists:
        raise GroupAlreadyExists


@group_router.delete(
    "/{group_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=None,
)
def delete_group(
    group_id: int,
    service: GroupService = Depends(group_service),
    # username=Depends(authenticate),
) -> None:
    try:
        service.delete_group(group_id)
    except EntityNotExists:
        raise GroupNotFound


@group_router.patch(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=GroupRead,
)
def update_group(
    group_id: int,
    group_input: GroupUpdate,
    service: GroupService = Depends(group_service),
    # username=Depends(authenticate),
) -> GroupRead:
    try:
        group: GroupRead = service.update_group(
            group_id=group_id,
            group_update=GroupUpdate(**group_input.dict()),
        )
        return group.dict()
    except EntityNotExists:
        raise GroupNotFound
