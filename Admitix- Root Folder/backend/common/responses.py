"""Consistent API response builders for routes that opt into an envelope."""

from __future__ import annotations

from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None, *, message: str | None = None, status_code: int = 200
) -> JSONResponse:
    """Return the standard successful response envelope."""

    body: dict[str, Any] = {"success": True, "data": jsonable_encoder(data)}
    if message is not None:
        body["message"] = message
    return JSONResponse(status_code=status_code, content=body)


def error_response(
    detail: Any, *, code: str = "bad_request", status_code: int = 400
) -> JSONResponse:
    """Return an error envelope compatible with ``common.exceptions``."""

    return JSONResponse(
        status_code=status_code,
        content={"success": False, "error": {"code": code, "detail": jsonable_encoder(detail)}},
    )
