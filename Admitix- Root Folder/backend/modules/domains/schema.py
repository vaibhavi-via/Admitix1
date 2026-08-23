"""Pydantic (v2) schemas for the `domains` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DomainBase(BaseModel):
    domain_code: str = Field(..., max_length=20, examples=["ENG"])
    domain_name: str = Field(..., max_length=100, examples=["Engineering"])
    description: str | None = None
    status: bool = True


class DomainCreate(DomainBase):
    """Payload for `POST /domains`."""


class DomainUpdate(BaseModel):
    """Payload for `PATCH /domains/{domain_id}` — every field optional."""

    domain_code: str | None = Field(None, max_length=20)
    domain_name: str | None = Field(None, max_length=100)
    description: str | None = None
    status: bool | None = None


class DomainRead(DomainBase):
    model_config = ConfigDict(from_attributes=True)

    domain_id: uuid.UUID
    created_at: datetime
