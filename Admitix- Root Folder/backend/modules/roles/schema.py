"""Pydantic (v2) schemas for the `roles` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    role_name: str = Field(..., max_length=50, examples=["admission_officer"])
    description: str | None = None


class RoleCreate(RoleBase):
    """Payload for `POST /roles`."""


class RoleUpdate(BaseModel):
    """Payload for `PATCH /roles/{role_id}` — every field optional."""

    role_name: str | None = Field(None, max_length=50)
    description: str | None = None


class RoleRead(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    role_id: uuid.UUID
    created_at: datetime
