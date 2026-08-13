"""Domain-specific exceptions for the `reports` module.

Reports has no dedicated table of its own — it only composes exports
from other modules' data — so the failure modes here are specific to
report generation rather than to a persisted record.
"""

from __future__ import annotations

from fastapi import HTTPException, status


class UnsupportedReportFormatException(HTTPException):
    """Raised when a requested `ReportFormat` cannot be rendered."""

    def __init__(self, detail: str = "This report format is not supported.") -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidReportDateRangeException(HTTPException):
    """Raised when `from_date` is after `to_date` in a report request."""

    def __init__(self, detail: str = "from_date must be before to_date.") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ReportGenerationException(HTTPException):
    """Raised when a report fails to render/export."""

    def __init__(self, detail: str = "Failed to generate the requested report.") -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
