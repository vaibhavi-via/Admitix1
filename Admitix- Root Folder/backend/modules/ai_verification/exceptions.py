"""Domain-specific exceptions for the `ai_verifications` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class AIVerificationNotFoundException(HTTPException):
    """Raised when an AI verification record id does not exist."""

    def __init__(self, detail: str = "AI verification record not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateAIVerificationException(HTTPException):
    """Raised when a document already has an AI verification record —
    mirrors `uq_ai_verifications_document_id` (one-to-one with
    `Document`)."""

    def __init__(
        self, detail: str = "This document already has an AI verification record."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidConfidenceScoreException(HTTPException):
    """Raised when `confidence_score` or `blur_score` falls outside
    0-100 — mirrors `ck_ai_verifications_confidence_score` /
    `ck_ai_verifications_blur_score`."""

    def __init__(self, detail: str = "Score values must be between 0 and 100.") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
