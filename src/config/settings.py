from functools import lru_cache
from os import environ
from typing import Any, Dict

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SharedWallet"

    # General
    ENVIRONMENT: str = environ.get("ENVIRONMENT", "development")
    PROJECT_NAME: str = "SharedWallet"
    PROJECT_VERSION: str = "0.1.0"
    CONTACT: Dict[str, str | Any] = {"email": "matias.brigante@gmail.com"}
    OPEN_API_URL: str = "/openapi.json"
    DEBUG: bool = bool(environ.get("DEBUG", 0))
    DATABASE_ECHO: bool = bool(environ.get("DATABASE_ECHO", 0))

    # JWT Auth
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "jwt-secret")

    # DataBase
    DB_ENGINE: str = environ.get("DB_ENGINE", "postgresql")
    DB_USER: str = environ.get("DB_USER", "postgres")
    DB_PASSWORD: str = environ.get("DB_PASSWORD", "postgres")
    DB_SERVER: str = environ.get("DB_SERVER", "postgres-sharedwallet")
    DB_PORT: str = environ.get("DB_PORT", "5432")
    DB_NAME: str = environ.get("DB_NAME")
    DATABASE_URI: str = (
        f"//{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    )
    DATABASE_URL: str = f"{DB_ENGINE}:{DATABASE_URI}"

    # CORS Middleware
    CORS_ORIGINS: list[str] = environ.get("CORS_ORIGINS", ["*"])
    CORS_ORIGINS_REGEX: str = environ.get("CORS_ORIGINS_REGEX", "")
    CORS_HEADERS: list[str] = environ.get("CORS_HEADERS", ["*"])

    # JWT
    # Token Generation
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("AT_EXPIRE_MINUTES", "60")
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 360


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
