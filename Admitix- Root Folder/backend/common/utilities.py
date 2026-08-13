"""Pure utility functions shared across modules."""

from __future__ import annotations

import re
from pathlib import Path


_SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")


def normalize_whitespace(value: str) -> str:
    """Trim a string and collapse internal whitespace to one space."""

    return " ".join(value.split())


def safe_filename(filename: str, *, default: str = "upload") -> str:
    """Remove path components and unsafe characters from an uploaded filename."""

    basename = Path(filename).name
    cleaned = _SAFE_FILENAME.sub("_", basename).strip("._")
    return cleaned or default


def mask_value(value: str, *, visible: int = 4, mask: str = "*") -> str:
    """Mask sensitive text while retaining the requested trailing characters."""

    if visible < 0:
        raise ValueError("visible must be zero or greater")
    if len(value) <= visible:
        return mask * len(value)
    return f"{mask * (len(value) - visible)}{value[-visible:]}"
