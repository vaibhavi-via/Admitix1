"""Domain-specific exceptions for the `departments` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class DepartmentNotFoundException(HTTPException):
    """Raised when a department id does not exist."""

    def __init__(self, detail: str = "Department not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
