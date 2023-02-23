# -*- coding: utf-8 -*-
"""Classes definition for User model."""
from sqlalchemy import Column
from sqlalchemy.dialects.oracle import VARCHAR2
from sqlalchemy.orm import Relationship

from src.pricetag.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    username = Column(VARCHAR2(255), primary_key=True)
    email = Column(VARCHAR2(255), unique=True, index=True)
    hashed_password = Column(VARCHAR2(255))
    disabled = Column(VARCHAR2(1), default="N")

    products = Relationship("Product", back_populates="user")
