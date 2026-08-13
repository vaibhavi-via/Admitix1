"""Domain-specific exceptions for the `notifications` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class NotificationNotFoundException(HTTPException):
    """Raised when a notification id does not exist."""

    def __init__(self, detail: str = "Notification not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
