# -*- coding: utf-8 -*-
"""Business logic for /user API endpoints."""

from sqlalchemy.orm import Session

from src.pricetag import models

from . import schema


async def get_product(db: Session, product_id: int) -> models.Product:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


async def get_products_by_user(
    db: Session, username: str, skip: int = 0, limit: int = 100
) -> models.Product:
    return (
        db.query(models.Product)
        .filter(models.Product.username == username)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_products_hist(
    db: Session, product_id: int, skip: int = 0, limit: int = 100
) -> models.ProductHist:
    return (
        db.query(models.ProductHist)
        .filter(models.ProductHist.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def create_product(db: Session, product: schema.ProductCreate) -> models.Product:
    db_product = models.Product(
        username=product.username,
        description=product.description,
        url=product.url,
        xpath=product.xpath,
        disabled=product.disabled,
        hist_size_days=product.hist_size_days,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


async def create_product_hist(
    db: Session, product_hist: schema.ProductHistCreate
) -> models.ProductHist:
    db_product_hist = models.ProductHist(
        product_id=product_hist.product_id,
        price=product_hist.price,
        date=product_hist.date,
    )
    db.add(db_product_hist)
    db.commit()
    db.refresh(db_product_hist)
    return db_product_hist
