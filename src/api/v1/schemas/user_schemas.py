from datetime import datetime
from pydantic import BaseModel


class UserFull(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserUpdate(BaseModel):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str
