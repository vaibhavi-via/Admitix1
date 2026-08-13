"""Pydantic (v2) schemas for the `reports` module.

Request/response shapes for generating exports. No dedicated table
backs this module.
"""

from __future__ import annotations

import uuid
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class ReportFormat(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"
    PDF = "pdf"


class AdmittedStudentsReportRequest(BaseModel):
    institution_id: uuid.UUID
    cycle_id: uuid.UUID
    course_id: uuid.UUID | None = None
    format: ReportFormat = ReportFormat.XLSX


class FeeCollectionReportRequest(BaseModel):
    institution_id: uuid.UUID
    from_date: date
    to_date: date
    format: ReportFormat = ReportFormat.XLSX


class ReportGeneratedResponse(BaseModel):
    file_name: str
    file_url: str
    generated_at: str = Field(..., description="ISO-8601 timestamp")
