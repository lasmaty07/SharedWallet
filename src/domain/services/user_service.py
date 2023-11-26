from typing import List
from sqlalchemy.orm import Session

from api.v1.schemas.user_schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
)


from domain.exceptions import EntityNotExists
from infrastructure.persistance.models.user import User
from infrastructure.persistance.repositories.user_repository import UserRepository
from passlib.context import CryptContext


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

    def create_user(
        self,
        user_create: UserCreate,
    ) -> UserRead:
        user_create.password == pwd_context.hash(user_create.password)
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

    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)
