"""Pydantic (v2) schemas for the `ai_verifications` resource."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from core.enums import AIVerificationStatus


class AIVerificationBase(BaseModel):
    ocr_text: str | None = None
    confidence_score: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    blur_score: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    missing_fields: str | None = None
    name_match: bool | None = None
    status: AIVerificationStatus = AIVerificationStatus.PENDING


class AIVerificationCreate(AIVerificationBase):
    """Payload used by the AI/OCR pipeline to record a verification
    result against a document."""

    document_id: uuid.UUID


class AIVerificationUpdate(BaseModel):
    ocr_text: str | None = None
    confidence_score: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    blur_score: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    missing_fields: str | None = None
    name_match: bool | None = None
    status: AIVerificationStatus | None = None
    verified_at: datetime | None = None


class AIVerificationRead(AIVerificationBase):
    model_config = ConfigDict(from_attributes=True)

    verification_id: uuid.UUID
    document_id: uuid.UUID
    verified_at: datetime | None
