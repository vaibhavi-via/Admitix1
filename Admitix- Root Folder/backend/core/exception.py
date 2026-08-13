"""Core exception registration for a predictable API error envelope."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "error": {"code": "validation_error", "detail": exc.errors()}},
    )


async def unhandled_error_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "error": {"code": "internal_error", "detail": "Internal server error."}},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Install exception handlers; call this during application setup if desired."""

    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
