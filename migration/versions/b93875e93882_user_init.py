# -*- coding: utf-8 -*-
"""User init

Revision ID: b93875e93882
Revises:
Create Date: 2023-02-19 16:45:22.718515

"""
import asyncio
import os

import sqlalchemy as sa
from alembic import op
from dotenv import load_dotenv
from sqlalchemy.dialects import oracle
from src.PriceTag.api.user.business import get_password_hash

load_dotenv()

# revision identifiers, used by Alembic.
revision = "b93875e93882"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = op.create_table(
        "users",
        sa.Column("username", oracle.VARCHAR2(length=255), nullable=False),
        sa.Column("email", oracle.VARCHAR2(length=255), nullable=True),
        sa.Column("hashed_password", oracle.VARCHAR2(length=255), nullable=True),
        sa.Column("disabled", oracle.VARCHAR2(length=1), nullable=True),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    # ### end Alembic commands ###

    password = asyncio.run(get_password_hash(os.environ.get("ADMIN_PASS")))

    op.bulk_insert(
        users_table,
        [
            {
                "username": os.environ.get("ADMIN_NAME"),
                "email": "admin@admin.com",
                "hashed_password": password,
                "disabled": "N",
            }
        ],
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###