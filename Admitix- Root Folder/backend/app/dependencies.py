"""Application-level FastAPI dependencies shared by route modules."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from common.pagination import PaginationParams
from db.session import get_db


DatabaseSession = Annotated[Session, Depends(get_db)]


def get_pagination(
    offset: int = 0,
    limit: int = 20,
) -> PaginationParams:
    """Validate common offset/limit query parameters for collection endpoints."""

    return PaginationParams(offset=offset, limit=limit)


Pagination = Annotated[PaginationParams, Depends(get_pagination)]


def get_request_id(
    request: Request,
    x_request_id: Annotated[str | None, Header()] = None,
) -> str:
    """Return the request id set by middleware, or the inbound header when present."""

    return getattr(request.state, "request_id", None) or x_request_id or ""
