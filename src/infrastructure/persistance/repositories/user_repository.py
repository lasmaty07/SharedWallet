from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.exceptions import EntityAlreadyExists
from infrastructure.persistance.models.user import User
from api.v1.schemas.user_schemas import (
    UserCreate,
    UserRead,
)


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def to_domain(user: User) -> UserRead:
        return UserRead(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            deleted_at=user.deleted_at,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
        )

    @staticmethod
    def to_persistance(user: UserCreate) -> User:
        return User(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
        )

    def add(self, user: User) -> UserRead:
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExists

        self.session.refresh(user)
        return user

    def get_all(self, page_size: int, page: int):
        users = self.session.execute(
            select(User)
            .where(User.deleted_at == None)
            .limit(page_size)
            .offset(page_size * page)
        ).all()
        return [user[0] for user in users]

    def get_without_map(self, user_id: int) -> User:
        user = self.session.execute(
            select(User).where(
                User.id == user_id,
                User.deleted_at == None,
            )
        ).first()
        if user:
            return user[0]

    def get(self, user_id: int) -> UserRead | None:
        user = self.session.execute(
            select(User).where(
                User.id == user_id,
                User.deleted_at == None,
            )
        ).first()
        if user:
            return self.to_domain(user[0])

    def get_password_by_email(self, user_email: str) -> str:
        user = self.session.execute(
            select(User).where(
                User.email == user_email,
                User.deleted_at == None,
            )
        ).first()
        if user:
            return user[0].password

    def get_user_by_email(self, user_email: str) -> int:
        user = self.session.execute(
            select(User).where(
                User.email == user_email,
                User.deleted_at == None,
            )
        ).first()
        if user:
            return user[0].id

    def update(self, user: User) -> UserRead:
        self.session.commit()
        self.session.refresh(user)
        return self.to_domain(user)

    def delete(self, user_id: int):
        user = self.session.execute(
            select(User).where(User.id == user_id)
        ).first()
        if user:
            user[0].deleted_at = datetime.now()
            self.session.commit()
            return True
        return False
