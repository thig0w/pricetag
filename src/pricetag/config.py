# -*- coding: utf-8 -*-
"""Config settings for for development, testing and production environments."""
import os
import secrets
from functools import lru_cache

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseSettings

load_dotenv()


class BaseAPISettings(BaseSettings):
    api_v1_route: str = "/api/v1"
    project_name: str = "pricetag"
    openapi_url: str = "/docs"
    redoc_url: str = "/redoc"
    debug: bool = False
    logger_level: str = "ERROR"

    # For the default, python-oracledb Thin mode that doesn't use Oracle Instant Client
    thick_mode: dict = None

    # To use python-oracledb Thick mode on macOS (Intel x86).
    # thick_mode = {"lib_dir": os.environ.get("HOME")+"/Downloads/instantclient_19_8"}

    # To use python-oracledb Thick mode on Windows
    # thick_mode = {"lib_dir": r"C:\oracle\instantclient_19_15"}

    # For thick mode on Linux use {} ie. no lib_dir parameter.  On Linux you
    # must configure the Instant Client directory by setting LD_LIBRARY_PATH or
    # running ldconfig before starting Python.
    # thick_mode = {}

    DB_USERNAME: str = os.environ.get("DB_USERNAME")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_CONNECT_ARGS: dict = (
        {"dsn": os.environ.get("DB_CONNECTSTRING")}
        if os.environ.get("DB_CONNECTSTRING") is not None
        else None
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL", f"oracle+oracledb://{DB_USERNAME}:{DB_PASSWORD}@"
    )

    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe()
    ALGORITHM = "HS256"

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


class DevAPISettings(BaseAPISettings):
    """Development configuration."""

    debug: bool = True
    logger_level: str = os.getenv("LOGGER_LEVEL", "TRACE")
    # 0 defalts to 10 seconds
    ACCESS_TOKEN_EXPIRE_MINUTES = 0


class TestAPISettings(BaseAPISettings):
    """Test configuration."""

    debug: bool = True
    logger_level: str = os.getenv("LOGGER_LEVEL", "DEBUG")
    ACCESS_TOKEN_EXPIRE_MINUTES = 10


class ProdAPISettings(BaseAPISettings):
    """Production configuration."""

    debug: bool = False
    logger_level: str = os.getenv("LOGGER_LEVEL", "ERROR")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


ENV_CONFIG_DICT = dict(
    development=DevAPISettings, testing=TestAPISettings, production=ProdAPISettings
)


@lru_cache()
def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProdAPISettings)()
