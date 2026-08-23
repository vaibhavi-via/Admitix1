"""Pydantic (v2) schemas for the `institutions` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class InstitutionBase(BaseModel):
    institution_name: str = Field(..., max_length=150)
    institution_code: str = Field(..., max_length=20)
    email: EmailStr = Field(..., max_length=150)
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    country: str = Field("India", max_length=100)
    logo_url: str | None = None
    domain_id: uuid.UUID | None = None
    status: bool = True


class InstitutionCreate(InstitutionBase):
    """Payload for `POST /institutions`."""


class InstitutionUpdate(BaseModel):
    """Payload for `PATCH /institutions/{institution_id}` — all optional."""

    institution_name: str | None = Field(None, max_length=150)
    institution_code: str | None = Field(None, max_length=20)
    email: EmailStr | None = Field(None, max_length=150)
    phone: str | None = Field(None, max_length=20)
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    logo_url: str | None = None
    domain_id: uuid.UUID | None = None
    status: bool | None = None


class InstitutionRead(InstitutionBase):
    model_config = ConfigDict(from_attributes=True)

    institution_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
