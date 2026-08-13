"""Pydantic (v2) schemas for the `faculties` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FacultyBase(BaseModel):
    faculty_name: str = Field(..., max_length=150)
    description: str | None = None
    status: bool = True


class FacultyCreate(FacultyBase):
    institution_id: uuid.UUID


class FacultyUpdate(BaseModel):
    faculty_name: str | None = Field(None, max_length=150)
    description: str | None = None
    status: bool | None = None


class FacultyRead(FacultyBase):
    model_config = ConfigDict(from_attributes=True)

    faculty_id: uuid.UUID
    institution_id: uuid.UUID
    created_at: datetime
