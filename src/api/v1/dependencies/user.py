from fastapi import Depends
from requests import Session

from infrastructure.persistance.base import get_session
from domain.services.user_service import UserService


def user_service(
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(session)
