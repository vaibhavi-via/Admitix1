"""Domain-specific exceptions for the `domains` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class DomainNotFoundException(HTTPException):
    """Raised when a domain id does not exist."""

    def __init__(self, detail: str = "Domain not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateDomainCodeException(HTTPException):
    """Raised when `domain_code` already belongs to another domain."""

    def __init__(
        self, detail: str = "This domain code is already in use."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class DomainInUseException(HTTPException):
    """Raised when attempting to delete a domain that is still assigned
    to existing institutions (`institutions.domain_id` is `ON DELETE
    RESTRICT`)."""

    def __init__(
        self, detail: str = "This domain is assigned to existing institutions and cannot be deleted."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
