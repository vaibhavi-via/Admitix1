"""Application startup and shutdown lifecycle management."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from core.config import APP_NAME
from core.logger import logger
from db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Log lifecycle events and release pooled database connections on shutdown.

    Schema creation and migrations deliberately remain outside the application
    process; Alembic owns those operations.
    """

    logger.info("Starting %s", APP_NAME)
    app.state.application_name = APP_NAME
    try:
        yield
    finally:
        engine.dispose()
        logger.info("Stopped %s", APP_NAME)
