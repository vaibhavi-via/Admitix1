"""Domain-specific exceptions for the `faculties` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class FacultyNotFoundException(HTTPException):
    """Raised when a faculty id does not exist."""

    def __init__(self, detail: str = "Faculty not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
