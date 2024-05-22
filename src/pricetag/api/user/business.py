# -*- coding: utf-8 -*-
"""Business logic for /user API endpoints."""
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from src.pricetag import config, models
from src.pricetag.db.session import get_db
from src.pricetag.models.security import TokenData

from .schema import UserCreate


async def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: UserCreate) -> models.User:
    hashed_password = await get_password_hash(user.password)
    db_user = models.User(
        username=user.email, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def verify_password(plain_password, hashed_password):
    return config.pwd_context.verify_password(plain_password, hashed_password)


async def get_password_hash(password):
    return config.pwd_context.hash_password(password)


async def authenticate_user(username: str, password: str, db: Session):
    user = await get_user(db, username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


##TODO: Validate permission access
async def get_current_user(
    token: str = Depends(config.oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise expired_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    if user.disabled == "Y":
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
