"""Reusable offset/limit pagination contracts and SQLAlchemy helper."""

from __future__ import annotations

from math import ceil
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session


ItemT = TypeVar("ItemT")


class PaginationParams(BaseModel):
    """Validated request parameters for offset-based collection endpoints."""

    offset: int = Field(default=0, ge=0, description="Number of records to skip.")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum records to return.")


class PageMeta(BaseModel):
    offset: int
    limit: int
    total: int
    page: int
    pages: int


class Page(BaseModel, Generic[ItemT]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: list[ItemT]
    meta: PageMeta


def build_page(items: Sequence[ItemT], *, total: int, offset: int, limit: int) -> Page[ItemT]:
    """Build a page from already-fetched items and a total count."""

    return Page(
        items=list(items),
        meta=PageMeta(
            offset=offset,
            limit=limit,
            total=total,
            page=(offset // limit) + 1,
            pages=ceil(total / limit) if total else 0,
        ),
    )


def paginate(db: Session, statement: Select[tuple[ItemT]], params: PaginationParams) -> Page[ItemT]:
    """Execute a SQLAlchemy select once for a count and once for the requested page."""

    count_statement = select(func.count()).select_from(statement.order_by(None).subquery())
    total = db.scalar(count_statement) or 0
    items = db.scalars(statement.offset(params.offset).limit(params.limit)).all()
    return build_page(items, total=total, offset=params.offset, limit=params.limit)
