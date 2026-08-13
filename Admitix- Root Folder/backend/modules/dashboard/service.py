"""Business logic for the `dashboard` module.

Read-only aggregation across other modules' ORM models
(`Application`, `Course`, `SeatMatrix`, `Payment`, `Document`). No
dedicated table backs this module, so every function here composes
its response directly from queries against those other models.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from core.enums import ApplicationCurrentStatus, DocumentVerificationStatus, PaymentStatus
from modules.applications.models import Application
from modules.courses.models import Course, SeatMatrix
from modules.documents.models import Document
from modules.payments.models import Payment


def get_dashboard_summary(db: Session) -> dict:
    """High-level counters for the landing dashboard view."""

    total_applications = db.query(func.count(Application.application_id)).scalar() or 0

    total_admitted = (
        db.query(func.count(Application.application_id))
        .filter(Application.current_status == ApplicationCurrentStatus.ADMITTED)
        .scalar()
        or 0
    )

    total_revenue_collected = (
        db.query(func.coalesce(func.sum(Payment.amount_paid), 0))
        .filter(Payment.payment_status == PaymentStatus.SUCCESS)
        .scalar()
        or 0
    )

    pending_document_verifications = (
        db.query(func.count(Document.document_id))
        .filter(Document.verification_status == DocumentVerificationStatus.PENDING)
        .scalar()
        or 0
    )

    return {
        "total_applications": total_applications,
        "total_admitted": total_admitted,
        "total_revenue_collected": float(total_revenue_collected),
        "pending_document_verifications": pending_document_verifications,
    }


def get_admission_statistics(db: Session) -> list[dict]:
    """Application funnel (count per `current_status`) grouped by
    admission cycle."""

    rows = (
        db.query(
            Application.cycle_id,
            Application.current_status,
            func.count(Application.application_id),
        )
        .group_by(Application.cycle_id, Application.current_status)
        .all()
    )

    funnels: dict = {}
    for cycle_id, current_status, count in rows:
        funnel = funnels.setdefault(
            cycle_id,
            {status.value: 0 for status in ApplicationCurrentStatus} | {"cycle_id": cycle_id},
        )
        funnel[current_status.value] = count

    return list(funnels.values())


def get_recent_applications(db: Session, limit: int = 10) -> list[Application]:
    """The most recently submitted applications."""

    return (
        db.query(Application)
        .order_by(Application.submission_date.desc())
        .limit(limit)
        .all()
    )


def get_payment_summary(db: Session) -> dict:
    """Aggregate payment totals grouped by status."""

    rows = (
        db.query(
            Payment.payment_status,
            func.count(Payment.payment_id),
            func.coalesce(func.sum(Payment.amount_paid), 0),
        )
        .group_by(Payment.payment_status)
        .all()
    )

    summary = {
        status.value: {"count": 0, "total_amount": 0.0} for status in PaymentStatus
    }
    for payment_status, count, total_amount in rows:
        summary[payment_status.value] = {
            "count": count,
            "total_amount": float(total_amount),
        }

    return summary


def get_document_statistics(db: Session) -> dict:
    """Document verification status breakdown."""

    rows = (
        db.query(Document.verification_status, func.count(Document.document_id))
        .group_by(Document.verification_status)
        .all()
    )

    stats = {status.value: 0 for status in DocumentVerificationStatus}
    for verification_status, count in rows:
        stats[verification_status.value] = count

    return stats


def get_seat_occupancy(db: Session) -> list[dict]:
    """Seat occupancy per course (bonus helper — not currently routed,
    but composed from the same data as `SeatOccupancySummary` in
    `schema.py` for future use)."""

    rows = (
        db.query(
            Course.course_id,
            Course.course_name,
            func.coalesce(func.sum(SeatMatrix.total_seats), 0),
            func.coalesce(func.sum(SeatMatrix.filled_seats), 0),
        )
        .outerjoin(SeatMatrix, SeatMatrix.course_id == Course.course_id)
        .group_by(Course.course_id, Course.course_name)
        .all()
    )

    return [
        {
            "course_id": course_id,
            "course_name": course_name,
            "total_seats": total_seats,
            "filled_seats": filled_seats,
            "available_seats": total_seats - filled_seats,
        }
        for course_id, course_name, total_seats, filled_seats in rows
    ]
