# -*- coding: utf-8 -*-
"""Parsers and serializers for /auth API endpoints."""
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    disabled: bool
