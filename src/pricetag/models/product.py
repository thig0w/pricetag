# -*- coding: utf-8 -*-
"""Classes definition for Product model."""
from sqlalchemy import Column, Date, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from src.pricetag.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), ForeignKey("users.username"), index=True)
    description = Column(String(255))
    url = Column(String(255))
    xpath = Column(String(255))
    disabled = Column(String(1), default="N")
    hist_size_days = Column(Integer, default=30)

    user = Relationship("User", back_populates="products")
    # prod_hist = Relationship("ProductHist", back_populates="product")


class ProductHist(Base):
    __tablename__ = "products_hist"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    price = Column(Double)
    date = Column(Date)

    # product = Relationship("Product", back_populates="products_hist")
