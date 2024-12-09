# -*- coding: utf-8 -*-
"""App initialization via factory pattern."""
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from .config import get_config

load_dotenv()
config = get_config(os.getenv("ENV"))

# logger.remove(0)
logger.add(sys.stderr, level=config.logger_level)
logger.info(f"Starting API for {config.project_name} with {config.__doc__}")


def create_app():
    logger.debug("Starting FastAPI")
    app = FastAPI(
        title=config.project_name,
        docs_url=config.openapi_url,
        redoc_url=config.redoc_url,
        openapi_tags=[],
        debug=config.debug,
        version="0.1.0",
    )

    logger.debug("Routing documentation to root")

    @app.get("/", include_in_schema=False)
    def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/docs")

    logger.debug("Adding User routes to FastAPI app")
    from src.pricetag.api import user

    app.include_router(user.endpoints.router, prefix=config.api_v1_route)
    app.openapi_tags += user.endpoints.tags_metadata

    logger.debug("Adding Product routes to FastAPI app")
    from src.pricetag.api import product

    app.include_router(product.endpoints.router, prefix=config.api_v1_route)
    app.openapi_tags += product.endpoints.tags_metadata

    logger.debug("Adding Exec routes to FastAPI app")
    from src.pricetag.api import exec

    app.include_router(exec.endpoints.router, prefix=config.api_v1_route)
    app.openapi_tags += exec.endpoints.tags_metadata

    logger.success("FastAPI app created!")
    return app
