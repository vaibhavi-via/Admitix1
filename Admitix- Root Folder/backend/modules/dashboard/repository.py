"""Read-model queries used by dashboard services."""

from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from modules.applications.models import Application
from modules.documents.models import Document
from modules.payments.models import Payment
from modules.students.models import Student


class DashboardRepository:
    def summary(self, db: Session, institution_id: object) -> dict[str, int]:
        """Return lightweight tenant-scoped dashboard totals."""
        application_count = db.scalar(
            select(func.count(Application.application_id))
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
        )
        document_count = db.scalar(
            select(func.count(Document.document_id))
            .join(Application, Document.application_id == Application.application_id)
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
        )
        payment_count = db.scalar(
            select(func.count(Payment.payment_id))
            .join(Application, Payment.application_id == Application.application_id)
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
        )
        return {
            "applications": application_count or 0,
            "documents": document_count or 0,
            "payments": payment_count or 0,
        }

    def application_statuses(self, db: Session, institution_id: object) -> list[dict[str, Any]]:
        rows = db.execute(
            select(Application.current_status, func.count(Application.application_id))
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
            .group_by(Application.current_status)
        ).all()
        return [{"status": status.value if hasattr(status, "value") else status, "count": count} for status, count in rows]
