"""General-purpose helpers that do not belong to a business module."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID


def to_jsonable(value: Any) -> Any:
    """Recursively convert common Python and ORM-friendly values to JSON types."""

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (datetime, date, UUID)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return to_jsonable(value.value)
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return to_jsonable(value.model_dump())
    return value


def compact_dict(values: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with ``None`` values removed, useful for partial updates."""

    return {key: value for key, value in values.items() if value is not None}
