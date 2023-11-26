from fastapi import Depends
from requests import Session

from infrastructure.persistance.base import get_session
from domain.services.group_service import GroupService


def group_service(
    session: Session = Depends(get_session),
) -> GroupService:
    return GroupService(session)
