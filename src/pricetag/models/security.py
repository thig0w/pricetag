# -*- coding: utf-8 -*-
"""Classes definition for Security Model."""

import bcrypt
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class CryptContext:
    # Hash a password using bcrypt
    def hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    # Check if the provided password matches the stored password (hashed)
    def verify_password(self, plain_password, hashed_password):
        password_byte_enc = plain_password.encode("utf-8")
        hashed_byte_enc = hashed_password.encode("utf-8")
        return bcrypt.checkpw(
            password=password_byte_enc, hashed_password=hashed_byte_enc
        )
