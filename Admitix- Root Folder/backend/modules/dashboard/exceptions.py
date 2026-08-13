"""Domain-specific exceptions for the `dashboard` module.

The dashboard has no dedicated table of its own — it only aggregates
data from other modules — so there are no "not found"/"duplicate"
style exceptions here. This is kept as a light placeholder for the one
failure mode that is specific to this module: an aggregation query
that cannot be computed as requested.
"""

from __future__ import annotations

from fastapi import HTTPException, status


class DashboardDataUnavailableException(HTTPException):
    """Raised when a dashboard aggregate cannot be computed (e.g. an
    upstream query failure), so the caller gets a clear 503 rather
    than a raw 500 traceback."""

    def __init__(
        self, detail: str = "Dashboard data is temporarily unavailable."
    ) -> None:
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
