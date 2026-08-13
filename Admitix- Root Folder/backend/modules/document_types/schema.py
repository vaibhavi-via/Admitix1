"""Pydantic (v2) schemas for the `document_types` resource."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field


class DocumentTypeBase(BaseModel):
    document_name: str = Field(..., max_length=100)
    mandatory: bool = True
    description: str | None = None


class DocumentTypeCreate(DocumentTypeBase):
    """Payload for `POST /document-types`."""


class DocumentTypeUpdate(BaseModel):
    document_name: str | None = Field(None, max_length=100)
    mandatory: bool | None = None
    description: str | None = None


class DocumentTypeRead(DocumentTypeBase):
    model_config = ConfigDict(from_attributes=True)

    document_type_id: uuid.UUID
