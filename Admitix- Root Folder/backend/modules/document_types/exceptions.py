"""Domain-specific exceptions for the `document_types` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class DocumentTypeNotFoundException(HTTPException):
    """Raised when a document type id does not exist."""

    def __init__(self, detail: str = "Document type not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DocumentTypeInUseException(HTTPException):
    """Raised when attempting to delete a document type that is still
    referenced by existing documents (`documents.document_type_id` is
    `ON DELETE RESTRICT`)."""

    def __init__(
        self,
        detail: str = "This document type is in use by existing documents and cannot be deleted.",
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
