"""Pydantic (v2) schemas for the `applications` module (applications,
application preferences, application status history)."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.enums import ApplicationCurrentStatus, PreferenceStatus


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class ApplicationBase(BaseModel):
    application_number: str = Field(..., max_length=30)
    current_status: ApplicationCurrentStatus = ApplicationCurrentStatus.DRAFT
    remarks: str | None = None


class ApplicationCreate(BaseModel):
    """Payload for `POST /applications`. `application_number` is
    generated server-side, so it is intentionally excluded here."""

    student_id: uuid.UUID
    cycle_id: uuid.UUID
    remarks: str | None = None


class ApplicationUpdate(BaseModel):
    current_status: ApplicationCurrentStatus | None = None
    reviewed_by: uuid.UUID | None = None
    remarks: str | None = None


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    application_id: uuid.UUID
    student_id: uuid.UUID
    cycle_id: uuid.UUID
    reviewed_by: uuid.UUID | None
    submission_date: datetime
    created_at: datetime


# ---------------------------------------------------------------------------
# Application Preference
# ---------------------------------------------------------------------------
class ApplicationPreferenceBase(BaseModel):
    preference_no: int = Field(..., gt=0)
    status: PreferenceStatus = PreferenceStatus.PENDING


class ApplicationPreferenceCreate(ApplicationPreferenceBase):
    application_id: uuid.UUID
    course_id: uuid.UUID


class ApplicationPreferenceUpdate(BaseModel):
    preference_no: int | None = Field(None, gt=0)
    status: PreferenceStatus | None = None


class ApplicationPreferenceRead(ApplicationPreferenceBase):
    model_config = ConfigDict(from_attributes=True)

    preference_id: uuid.UUID
    application_id: uuid.UUID
    course_id: uuid.UUID


# ---------------------------------------------------------------------------
# Application Status History (read-only audit trail)
# ---------------------------------------------------------------------------
class ApplicationStatusHistoryCreate(BaseModel):
    """Used internally by the service layer when recording a status
    transition — not intended to be exposed as a public write
    endpoint. `institution_id` may be omitted; the DB trigger fills it
    in from the parent application's student when absent."""

    application_id: uuid.UUID
    institution_id: uuid.UUID | None = None
    old_status: str | None = Field(None, max_length=30)
    new_status: str = Field(..., max_length=30)
    changed_by: uuid.UUID | None = None
    remarks: str | None = None


class ApplicationStatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    history_id: uuid.UUID
    application_id: uuid.UUID
    institution_id: uuid.UUID
    old_status: str | None
    new_status: str
    changed_by: uuid.UUID | None
    remarks: str | None
    changed_at: datetime
