"""Pydantic (v2) schemas for the `users` module (users, staff)."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
class UserBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr = Field(..., max_length=150)
    phone: str | None = Field(None, max_length=20)
    profile_photo: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    """Payload for `POST /users`. `password` is hashed by the service
    layer before persistence — never store or accept `password_hash`
    directly from a client."""

    institution_id: uuid.UUID | None = None
    role_id: uuid.UUID
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr | None = Field(None, max_length=150)
    phone: str | None = Field(None, max_length=20)
    profile_photo: str | None = None
    is_active: bool | None = None
    role_id: uuid.UUID | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    institution_id: uuid.UUID | None
    role_id: uuid.UUID
    last_login: datetime | None
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Staff
# ---------------------------------------------------------------------------
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
    designation: str | None = Field(None, max_length=100)
    joining_date: date | None = None
    department_id: uuid.UUID | None = None
    status: bool | None = None


class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)

    staff_id: uuid.UUID
    user_id: uuid.UUID
    institution_id: uuid.UUID
    department_id: uuid.UUID | None
