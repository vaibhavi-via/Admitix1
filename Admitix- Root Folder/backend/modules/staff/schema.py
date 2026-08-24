from __future__ import annotations
import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StaffBase(BaseModel):
    employee_id: str = Field(..., max_length=50)
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    status: bool = True

class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)
    staff_id: uuid.UUID
    user_id: uuid.UUID
    institution_id: uuid.UUID
    department_id: uuid.UUID | None

class StaffCreate(StaffBase):
    user_id: uuid.UUID
    institution_id: uuid.UUID
    department_id: uuid.UUID | None = None

class StaffAccountCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    institution_id: uuid.UUID
    department_id: uuid.UUID | None = None
    employee_id: str = Field(..., min_length=1, max_length=50)
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    role_name: str = Field(default="admission_officer", max_length=50)

class StaffAccountRead(BaseModel):
    staff: StaffRead
    activation_token: str | None = None
    activation_expires_in_hours: int

class StaffUpdate(BaseModel):
    department_id: uuid.UUID | None = None
    employee_id: str | None = Field(None, max_length=50)
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    status: bool | None = None
