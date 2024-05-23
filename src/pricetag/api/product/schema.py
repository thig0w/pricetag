# -*- coding: utf-8 -*-
"""Parsers and serializers for /product API endpoints."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    username: str
    description: str
    url: str
    xpath: str
    disabled: str | None = Field(default="N", title="Product checking disabled?")
    hist_size_days: int | None = Field(default=30, title="Days to hold History data")


class Product(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductHistCreateBase(BaseModel):
    price: float | None = Field(gt=0, description="The price must be greater than zero")
    date: datetime


class ProductHistCreate(ProductHistCreateBase):
    product_id: int


class ProductHist(ProductHistCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
