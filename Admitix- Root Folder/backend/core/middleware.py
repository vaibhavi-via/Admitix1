"""Optional FastAPI middleware for request tracing and structured request logs."""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from core.logger import logger


async def request_context_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Attach a request id and log request completion without consuming its body."""

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started_at = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "%s %s -> %s (%.3fs) request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        time.perf_counter() - started_at,
        request_id,
    )
    return response
