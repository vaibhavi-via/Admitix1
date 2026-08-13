"""Pydantic (v2) schemas for the `courses` module (courses, fee
structure, seat matrix)."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------
class CourseBase(BaseModel):
    course_name: str = Field(..., max_length=150)
    course_code: str = Field(..., max_length=30)
    duration_years: int = Field(..., gt=0)
    eligibility: str | None = None
    status: bool = True


class CourseCreate(CourseBase):
    department_id: uuid.UUID
    institution_id: uuid.UUID


class CourseUpdate(BaseModel):
    course_name: str | None = Field(None, max_length=150)
    course_code: str | None = Field(None, max_length=30)
    duration_years: int | None = Field(None, gt=0)
    eligibility: str | None = None
    status: bool | None = None


class CourseRead(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    course_id: uuid.UUID
    department_id: uuid.UUID
    institution_id: uuid.UUID
    # Read-only: maintained by a DB trigger from `seat_matrix.total_seats`.
    total_seats: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Fee Structure
# ---------------------------------------------------------------------------
class FeeStructureBase(BaseModel):
    category: str = Field(..., max_length=30)
    tuition_fee: Decimal = Field(Decimal("0"), ge=0, decimal_places=2)
    admission_fee: Decimal = Field(Decimal("0"), ge=0, decimal_places=2)
    other_fee: Decimal = Field(Decimal("0"), ge=0, decimal_places=2)
    effective_from: date


class FeeStructureCreate(FeeStructureBase):
    course_id: uuid.UUID


class FeeStructureUpdate(BaseModel):
    category: str | None = Field(None, max_length=30)
    tuition_fee: Decimal | None = Field(None, ge=0, decimal_places=2)
    admission_fee: Decimal | None = Field(None, ge=0, decimal_places=2)
    other_fee: Decimal | None = Field(None, ge=0, decimal_places=2)
    effective_from: date | None = None


class FeeStructureRead(FeeStructureBase):
    model_config = ConfigDict(from_attributes=True)

    fee_id: uuid.UUID
    course_id: uuid.UUID
    # Read-only: DB-generated column (tuition_fee + admission_fee + other_fee).
    total_fee: Decimal


# ---------------------------------------------------------------------------
# Seat Matrix
# ---------------------------------------------------------------------------
class SeatMatrixBase(BaseModel):
    category: str = Field(..., max_length=30)
    total_seats: int = Field(..., ge=0)
    filled_seats: int = Field(0, ge=0)


class SeatMatrixCreate(SeatMatrixBase):
    course_id: uuid.UUID


class SeatMatrixUpdate(BaseModel):
    total_seats: int | None = Field(None, ge=0)
    filled_seats: int | None = Field(None, ge=0)


class SeatMatrixRead(SeatMatrixBase):
    model_config = ConfigDict(from_attributes=True)

    seat_id: uuid.UUID
    course_id: uuid.UUID
    # Read-only: DB-generated column (total_seats - filled_seats).
    available_seats: int
