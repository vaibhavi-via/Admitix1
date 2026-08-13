from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
class EntranceExamScoreBase(BaseModel):
    exam_name: str = Field(..., max_length=100)
    roll_number: str | None = Field(None, max_length=50)
    score: Decimal | None = Field(None, decimal_places=2)
    percentile: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    rank: int | None = Field(None, gt=0)
    exam_year: int | None = Field(None, ge=1950, le=2100)
class EntranceExamScoreCreate(EntranceExamScoreBase): student_id: uuid.UUID
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
