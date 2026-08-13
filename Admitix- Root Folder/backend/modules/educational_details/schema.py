from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class EducationDetailBase(BaseModel):
    qualification: str = Field(..., max_length=100)
    board_university: str | None = Field(None, max_length=150)
    institution_name: str | None = Field(None, max_length=150)
    passing_year: int | None = Field(None, ge=1950, le=2100)
    seat_number: str | None = Field(None, max_length=50)
    percentage: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    cgpa: Decimal | None = Field(None, ge=0, le=10, decimal_places=2)
class EducationDetailCreate(EducationDetailBase): student_id: uuid.UUID
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
