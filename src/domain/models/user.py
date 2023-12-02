from datetime import datetime
from dataclasses import dataclass

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class User:
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
