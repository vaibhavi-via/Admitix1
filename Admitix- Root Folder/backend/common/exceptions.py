"""Application-wide exception types and FastAPI exception handlers."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


class AppException(Exception):
    """Base exception for predictable API errors."""

    def __init__(
        self,
        detail: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "bad_request",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.code = code
        self.headers = headers
        super().__init__(detail)


class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found.") -> None:
        super().__init__(detail, status_code=status.HTTP_404_NOT_FOUND, code="not_found")


class ConflictError(AppException):
    def __init__(self, detail: str = "Resource already exists.") -> None:
        super().__init__(detail, status_code=status.HTTP_409_CONFLICT, code="conflict")


class ForbiddenError(AppException):
    def __init__(self, detail: str = "You do not have permission to perform this action.") -> None:
        super().__init__(detail, status_code=status.HTTP_403_FORBIDDEN, code="forbidden")


def _error_body(*, code: str, detail: Any) -> dict[str, Any]:
    return {"success": False, "error": {"code": code, "detail": detail}}


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(code=exc.code, detail=exc.detail),
        headers=exc.headers,
    )


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_body(code="validation_error", detail=exc.errors()),
    )


async def integrity_exception_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=_error_body(code="integrity_error", detail="The request conflicts with existing data."),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register the optional standard error format on a FastAPI app."""

    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)
