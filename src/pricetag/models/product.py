# -*- coding: utf-8 -*-
"""Classes definition for Product model."""
from sqlalchemy import Column, ForeignKey, Sequence
from sqlalchemy.dialects.oracle import DATE, NUMBER, VARCHAR2
from sqlalchemy.orm import Relationship

from src.pricetag.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(NUMBER(10), Sequence("products_seq"), primary_key=True)
    username = Column(VARCHAR2(255), ForeignKey("users.username"), index=True)
    description = Column(VARCHAR2(255))
    url = Column(VARCHAR2(255))
    xpath = Column(VARCHAR2(255))
    disabled = Column(VARCHAR2(1), default="N")
    hist_size_days = Column(NUMBER(10), default=30)

    user = Relationship("User", back_populates="products")
    # prod_hist = Relationship("ProductHist", back_populates="product")


class ProductHist(Base):
    __tablename__ = "products_hist"

    id = Column(NUMBER(10), Sequence("products_hist_seq"), primary_key=True)
    product_id = Column(NUMBER(10), ForeignKey("products.id"), index=True)
    price = Column(NUMBER(10, 2))
    date = Column(DATE)

    # product = Relationship("Product", back_populates="products_hist")
