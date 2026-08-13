from __future__ import annotations

import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class StaffBase(BaseModel):
    employee_id: str = Field(..., max_length=50)
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    status: bool = True


class StaffCreate(StaffBase):
    user_id: uuid.UUID
    institution_id: uuid.UUID
    department_id: uuid.UUID | None = None


class StaffUpdate(BaseModel):
    department_id: uuid.UUID | None = None
    employee_id: str | None = Field(None, max_length=50)
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    status: bool | None = None


class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)
    staff_id: uuid.UUID
    user_id: uuid.UUID
    institution_id: uuid.UUID
    department_id: uuid.UUID | None
