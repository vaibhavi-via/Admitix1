"""Pydantic (v2) schemas for the `admission_cycles` resource."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.enums import AdmissionCycleStatus


class AdmissionCycleBase(BaseModel):
    academic_year: str = Field(..., max_length=20, examples=["2026-27"])
    application_start: date
    application_end: date
    status: AdmissionCycleStatus = AdmissionCycleStatus.UPCOMING

    @model_validator(mode="after")
    def _validate_date_range(self) -> "AdmissionCycleBase":
        if self.application_end <= self.application_start:
            raise ValueError("application_end must be after application_start")
        return self


class AdmissionCycleCreate(AdmissionCycleBase):
    institution_id: uuid.UUID


class AdmissionCycleUpdate(BaseModel):
    academic_year: str | None = Field(None, max_length=20)
    application_start: date | None = None
    application_end: date | None = None
    status: AdmissionCycleStatus | None = None


class AdmissionCycleRead(AdmissionCycleBase):
    model_config = ConfigDict(from_attributes=True)

    cycle_id: uuid.UUID
    institution_id: uuid.UUID
    created_at: datetime
