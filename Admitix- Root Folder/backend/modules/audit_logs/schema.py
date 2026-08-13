"""Pydantic (v2) schemas for the `audit_logs` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditLogBase(BaseModel):
    action: str = Field(..., max_length=50, examples=["UPDATE"])
    table_name: str = Field(..., max_length=100, examples=["applications"])
    record_id: uuid.UUID | None = None
    ip_address: str | None = Field(None, max_length=45)


class AuditLogCreate(AuditLogBase):
    """Payload used internally by the service layer / middleware when
    recording an action. `institution_id` may be omitted; the DB
    trigger fills it in from `user_id` when absent."""

    user_id: uuid.UUID | None = None
    institution_id: uuid.UUID | None = None


class AuditLogRead(AuditLogBase):
    model_config = ConfigDict(from_attributes=True)

    log_id: uuid.UUID
    user_id: uuid.UUID | None
    institution_id: uuid.UUID | None
    created_at: datetime
