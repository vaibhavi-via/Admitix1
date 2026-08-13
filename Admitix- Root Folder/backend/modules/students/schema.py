"""Pydantic (v2) schemas for the `students` module (students, education
details, entrance exam scores)."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.enums import Gender


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------
class StudentBase(BaseModel):
    aadhaar_no: str | None = Field(None, max_length=20)
    gender: Gender | None = None
    dob: date | None = None
    blood_group: str | None = Field(None, max_length=5)
    category: str | None = Field(None, max_length=30)
    nationality: str = Field("Indian", max_length=50)
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)
    parent_name: str | None = Field(None, max_length=150)
    parent_phone: str | None = Field(None, max_length=20)
    guardian_email: EmailStr | None = Field(None, max_length=150)


class StudentCreate(StudentBase):
    user_id: uuid.UUID
    institution_id: uuid.UUID


class StudentUpdate(BaseModel):
    aadhaar_no: str | None = Field(None, max_length=20)
    gender: Gender | None = None
    dob: date | None = None
    blood_group: str | None = Field(None, max_length=5)
    category: str | None = Field(None, max_length=30)
    nationality: str | None = Field(None, max_length=50)
    address: str | None = None
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)
    parent_name: str | None = Field(None, max_length=150)
    parent_phone: str | None = Field(None, max_length=20)
    guardian_email: EmailStr | None = Field(None, max_length=150)


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    student_id: uuid.UUID
    user_id: uuid.UUID
    institution_id: uuid.UUID
    created_at: datetime


# ---------------------------------------------------------------------------
# Education Detail
# ---------------------------------------------------------------------------
class EducationDetailBase(BaseModel):
    qualification: str = Field(..., max_length=100)
    board_university: str | None = Field(None, max_length=150)
    institution_name: str | None = Field(None, max_length=150)
    passing_year: int | None = Field(None, ge=1950, le=2100)
    seat_number: str | None = Field(None, max_length=50)
    percentage: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    cgpa: Decimal | None = Field(None, ge=0, le=10, decimal_places=2)


class EducationDetailCreate(EducationDetailBase):
    student_id: uuid.UUID


class EducationDetailUpdate(BaseModel):
    qualification: str | None = Field(None, max_length=100)
    board_university: str | None = Field(None, max_length=150)
    institution_name: str | None = Field(None, max_length=150)
    passing_year: int | None = Field(None, ge=1950, le=2100)
    seat_number: str | None = Field(None, max_length=50)
    percentage: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    cgpa: Decimal | None = Field(None, ge=0, le=10, decimal_places=2)


class EducationDetailRead(EducationDetailBase):
    model_config = ConfigDict(from_attributes=True)

    education_id: uuid.UUID
    student_id: uuid.UUID
    created_at: datetime


# ---------------------------------------------------------------------------
# Entrance Exam Score
# ---------------------------------------------------------------------------
class EntranceExamScoreBase(BaseModel):
    exam_name: str = Field(..., max_length=100)
    roll_number: str | None = Field(None, max_length=50)
    score: Decimal | None = Field(None, decimal_places=2)
    percentile: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    rank: int | None = Field(None, gt=0)
    exam_year: int | None = Field(None, ge=1950, le=2100)


class EntranceExamScoreCreate(EntranceExamScoreBase):
    student_id: uuid.UUID


class EntranceExamScoreUpdate(BaseModel):
    exam_name: str | None = Field(None, max_length=100)
    roll_number: str | None = Field(None, max_length=50)
    score: Decimal | None = Field(None, decimal_places=2)
    percentile: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    rank: int | None = Field(None, gt=0)
    exam_year: int | None = Field(None, ge=1950, le=2100)


class EntranceExamScoreRead(EntranceExamScoreBase):
    model_config = ConfigDict(from_attributes=True)

    score_id: uuid.UUID
    student_id: uuid.UUID
    created_at: datetime
