"""Idempotent logging configuration for application entry points and workers."""

from __future__ import annotations

import logging
from pathlib import Path

from core.config import LOG_FILE, LOG_LEVEL


def configure_logging(name: str = "Admitix") -> logging.Logger:
    """Configure and return a named logger without adding duplicate handlers."""

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
