"""Pydantic (v2) schemas for the `documents` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.enums import DocumentVerificationStatus


class DocumentBase(BaseModel):
    file_name: str = Field(..., max_length=255)
    file_url: str
    remarks: str | None = None


class DocumentCreate(DocumentBase):
    application_id: uuid.UUID
    document_type_id: uuid.UUID


class DocumentUpdate(BaseModel):
    verification_status: DocumentVerificationStatus | None = None
    verified_by: uuid.UUID | None = None
    remarks: str | None = None


class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    document_id: uuid.UUID
    application_id: uuid.UUID
    document_type_id: uuid.UUID
    verification_status: DocumentVerificationStatus
    verified_by: uuid.UUID | None
    uploaded_at: datetime
