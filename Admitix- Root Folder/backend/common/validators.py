"""Composable validation helpers for module schemas and services."""

from __future__ import annotations

import re
from collections.abc import Iterable

from common.utilities import normalize_whitespace


def require_non_empty(value: str, *, field_name: str = "value", max_length: int | None = None) -> str:
    """Normalize a required text field and enforce an optional maximum length."""

    normalized = normalize_whitespace(value)
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    if max_length is not None and len(normalized) > max_length:
        raise ValueError(f"{field_name} must not exceed {max_length} characters")
    return normalized


def require_unique(values: Iterable[object], *, field_name: str = "values") -> None:
    """Raise when a collection contains duplicate non-hashable-safe values."""

    items = list(values)
    if len({repr(item) for item in items}) != len(items):
        raise ValueError(f"{field_name} must not contain duplicates")


def validate_phone_number(value: str, *, field_name: str = "phone number") -> str:
    """Accept an international phone number containing 7 to 15 digits."""

    normalized = re.sub(r"[\s()-]", "", value)
    if not re.fullmatch(r"\+?[0-9]{7,15}", normalized):
        raise ValueError(f"Invalid {field_name}")
    return normalized
