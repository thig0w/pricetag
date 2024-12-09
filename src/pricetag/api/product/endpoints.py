# -*- coding: utf-8 -*-
"""API endpoint definitions for /user namespace."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.pricetag.api.user.business import get_current_user, get_user
from src.pricetag.api.user.schema import User
from src.pricetag.db.session import get_db

from . import business, schema

tags_metadata = [
    {"name": "product", "description": "Product Control edpoints"},
]

router = APIRouter(
    prefix="/products",
    responses={
        404: {"description": "Not found"},
        505: {"description": "Internal Server Error"},
    },
)


@router.post("/", response_model=schema.Product, tags=["product"])
async def create_product(
    product: schema.ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = await get_user(db, username=product.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await business.create_product(db=db, product=product)


@router.get("/", response_model=list[schema.Product], tags=["product"])
async def read_user_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = await business.get_products_by_user(
        db=db, username=current_user.username, skip=skip, limit=limit
    )
    return products


@router.get("/{product_id}", response_model=schema.Product, tags=["product"])
async def read_product_info_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = await business.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product id Not Found")
    return db_product


# TODO: create role - just admin should trigger execute all
@router.get("/execute", response_model=schema.Product, tags=["product"])
async def send_exec_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: Implement
    db_product = await business.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product id Not Found")
    return db_product


@router.get("/execute/{user}", response_model=schema.Product, tags=["product"])
async def send_exec_product_user(
    product_id: int,
    user: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: Implement
    db_product = await business.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product id Not Found")
    return db_product


@router.get(
    "/execute/{user}/{product_id}", response_model=schema.Product, tags=["product"]
)
async def send_exec_product_user_id(
    product_id: int,
    user: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: Implement
    db_product = await business.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product id Not Found")
    return db_product
