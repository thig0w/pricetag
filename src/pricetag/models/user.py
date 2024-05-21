# -*- coding: utf-8 -*-
"""Classes definition for User model."""

from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship

from src.pricetag.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    disabled = Column(String(1), default="N")

    products = Relationship("Product", back_populates="user")
