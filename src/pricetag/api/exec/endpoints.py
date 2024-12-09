# -*- coding: utf-8 -*-
"""API endpoint definitions for /user namespace."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.pricetag.api.user.business import get_current_user
from src.pricetag.api.user.schema import User
from src.pricetag.db.session import get_db

from . import business

tags_metadata = [
    {"name": "execution", "description": "Execution Control edpoints"},
]

router = APIRouter(
    prefix="/exec",
    responses={
        404: {"description": "Not found"},
        505: {"description": "Internal Server Error"},
    },
)

# TODO: protect path, just admin
@router.get("/{product_id}", tags=["execution"])
async def read_product_info(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    price = await business.get_price_for_product(db, product_id=product_id)
    if price is None:
        raise HTTPException(status_code=404, detail="Product id Not Found")
    return price
