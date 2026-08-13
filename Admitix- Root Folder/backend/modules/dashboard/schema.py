"""Pydantic (v2) schemas for the `dashboard` module.

Read-only aggregate/summary shapes composed from other modules' data.
No dedicated table backs this module.
"""

from __future__ import annotations

import uuid

from pydantic import BaseModel


class ApplicationFunnelSummary(BaseModel):
    """Count of applications per `current_status` for an institution
    within an admission cycle."""

    cycle_id: uuid.UUID
    draft: int = 0
    submitted: int = 0
    under_review: int = 0
    documents_pending: int = 0
    approved: int = 0
    rejected: int = 0
    admitted: int = 0
    cancelled: int = 0


class SeatOccupancySummary(BaseModel):
    course_id: uuid.UUID
    course_name: str
    total_seats: int
    filled_seats: int
    available_seats: int


class InstitutionDashboardSummary(BaseModel):
    institution_id: uuid.UUID
    total_applications: int
    total_admitted: int
    total_revenue_collected: float
    pending_document_verifications: int
