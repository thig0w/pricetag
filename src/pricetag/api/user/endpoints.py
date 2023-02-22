# -*- coding: utf-8 -*-
"""API endpoint definitions for /user namespace."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.pricetag import config
from src.pricetag.db.session import get_db
from src.pricetag.models.security import Token

from . import business, schema

tags_metadata = [
    {"name": "auth", "description": "Authentication edpoints"},
    {"name": "users", "description": "User Operations"},
]

router = APIRouter(
    prefix="/users",
    responses={
        404: {"description": "Not found"},
        505: {"description": "Internal Server Error"},
    },
)


@router.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await business.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await business.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=schema.User, tags=["users"])
async def create_user(
    user: schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(business.get_current_user),
):
    db_user = await business.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = await business.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await business.create_user(db=db, user=user)


@router.get("/", response_model=list[schema.User], tags=["users"])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(business.get_current_user),
):
    users = await business.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{username}", response_model=schema.User, tags=["users"])
async def read_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: schema.User = Depends(business.get_current_user),
):
    db_user = await business.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/me/", response_model=schema.User, tags=["users"])
async def read_users_me(current_user: schema.User = Depends(business.get_current_user)):
    return current_user
