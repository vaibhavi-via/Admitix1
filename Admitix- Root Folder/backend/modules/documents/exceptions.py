"""Domain-specific exceptions for the `documents` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class DocumentNotFoundException(HTTPException):
    """Raised when a document id does not exist."""

    def __init__(self, detail: str = "Document not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidVerificationStatusTransitionException(HTTPException):
    """Raised when a requested `verification_status` change is not a
    valid transition (e.g. re-verifying an already `verified`
    document without first requesting a reupload)."""

    def __init__(
        self, detail: str = "This verification status transition is not allowed."
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class DocumentVerifierRequiredException(HTTPException):
    """Raised when `verification_status` is being set to `verified` or
    `rejected` without a `verified_by` user supplied."""

    def __init__(
        self, detail: str = "verified_by is required when setting this verification status."
    ) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
