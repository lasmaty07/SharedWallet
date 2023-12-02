from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from api.v1.schemas.user_schemas import (
    TokenResponse,
    UserLogin,
    UserRead,
    UserCreate,
    UserUpdate,
    UserFull,
)
from domain.exceptions import EntityNotExists, IncorrectPassword
from infrastructure.persistance.models.user import User
from infrastructure.persistance.repositories.user_repository import (
    UserRepository,
)

from config.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = UserRepository(self.session)

    def get_users(self, page_size: int, page: int) -> List[UserCreate]:
        return [
            self.repository.to_domain(user)
            for user in self.repository.get_all(page_size, page)
        ]

    def get_user(self, user_id: int) -> UserRead:
        instance: User = self.repository.get(user_id)
        if not instance:
            raise EntityNotExists
        user_read = self.repository.to_domain(instance)
        return user_read

    def get_user_by_email(self, user_email: str) -> UserFull:
        instance: User = self.repository.get_password_by_email(user_email)
        if not instance:
            raise EntityNotExists
        user_full = self.repository.to_domain(instance)
        return user_full

    def create_user(
        self,
        user_create: UserCreate,
    ) -> UserRead:
        user_create.email = user_create.email.lower()
        user_create.password = pwd_context.hash(user_create.password)
        user = self.repository.to_persistance(user_create)
        user_read = self.repository.add(user)
        return user_read

    def update_user(
        self,
        user_id: int,
        user_update: UserUpdate,
    ) -> UserRead:
        user: User = self.repository.get_without_map(user_id)
        if not user:
            raise EntityNotExists
        for k, v in user_update.dict(exclude_unset=True).items():
            if v:
                setattr(user, k, v)
        user_read = self.repository.update(user)
        return user_read

    def delete_user(self, user_id: int) -> None:
        return self.repository.delete(user_id)

    def authenticate_user(self, user_login: UserLogin) -> TokenResponse:
        user = self.repository.get_user_by_email(user_login.email)
        if not user.check_password(user_login.password):
            raise IncorrectPassword

        return self.create_token(user_login.email)

    def create_token(self, user_email: str) -> TokenResponse:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire, "email": user_email}

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return {
            "access_token": encoded_jwt,
            "token_type": "bearer",
        }
