"""Small, allowlist-based helpers for SQLAlchemy list filters and sorting."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeBase


ModelT = TypeVar("ModelT", bound=DeclarativeBase)


def apply_filters(
    statement: Select[tuple[ModelT]], model: type[ModelT], filters: Mapping[str, Any] | None
) -> Select[tuple[ModelT]]:
    """Apply equality filters only for mapped columns with non-``None`` values."""

    if not filters:
        return statement
    columns = {column.key for column in model.__table__.columns}
    unknown = set(filters) - columns
    if unknown:
        raise ValueError(f"Unknown {model.__name__} filter fields: {sorted(unknown)}")
    return statement.filter_by(**{key: value for key, value in filters.items() if value is not None})


def apply_sorting(
    statement: Select[tuple[ModelT]],
    model: type[ModelT],
    *,
    sort_by: str | None = None,
    descending: bool = False,
    allowed_fields: Iterable[str] | None = None,
) -> Select[tuple[ModelT]]:
    """Apply a validated sort field; callers may further restrict sortable columns."""

    if not sort_by:
        return statement
    permitted = set(allowed_fields or (column.key for column in model.__table__.columns))
    if sort_by not in permitted or not hasattr(model, sort_by):
        raise ValueError(f"Unsupported {model.__name__} sort field: {sort_by}")
    field = getattr(model, sort_by)
    return statement.order_by(field.desc() if descending else field.asc())
