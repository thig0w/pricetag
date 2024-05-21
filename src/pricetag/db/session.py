# -*- coding: utf-8 -*-
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.pricetag import config

logger.debug("Creating DB engine")
logger.trace(
    f"DB engine Configs:\
        {config.DATABASE_URL} - {config.DB_CONNECT_ARGS}"
)
engine = create_engine(
    config.DATABASE_URL,
    # thick_mode=config.thick_mode,
    # connect_args=config.DB_CONNECT_ARGS,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: Remove this when alembic is ready
# Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
