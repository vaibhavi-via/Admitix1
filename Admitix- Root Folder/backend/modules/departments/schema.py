"""Pydantic (v2) schemas for the `departments` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DepartmentBase(BaseModel):
    department_name: str = Field(..., max_length=150)
    hod_staff_id: uuid.UUID | None = None
    description: str | None = None
    status: bool = True


class DepartmentCreate(DepartmentBase):
    faculty_id: uuid.UUID
    institution_id: uuid.UUID


class DepartmentUpdate(BaseModel):
    department_name: str | None = Field(None, max_length=150)
    hod_staff_id: uuid.UUID | None = None
    description: str | None = None
    status: bool | None = None


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    department_id: uuid.UUID
    faculty_id: uuid.UUID
    institution_id: uuid.UUID
    created_at: datetime
