"""Domain-specific exceptions for the `institutions` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class InstitutionNotFoundException(HTTPException):
    """Raised when an institution id does not exist."""

    def __init__(self, detail: str = "Institution not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateInstitutionCodeException(HTTPException):
    """Raised when `institution_code` already belongs to another
    institution."""

    def __init__(
        self, detail: str = "This institution code is already in use."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InstitutionDeactivatedException(HTTPException):
    """Raised when an operation is attempted against an institution
    whose `status` is inactive (`false`)."""

    def __init__(self, detail: str = "This institution has been deactivated.") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
