"""Read-model queries used to build institution-scoped reports."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from modules.applications.models import Application
from modules.documents.models import Document
from modules.payments.models import Payment
from modules.students.models import Student


class ReportsRepository:
    """Provides query statements; formatting/export belongs in the service layer."""

    def admissions(self, institution_id: object) -> Select[tuple[Application]]:
        return (
            select(Application)
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
            .order_by(Application.submission_date.desc())
        )

    def payments(self, institution_id: object) -> Select[tuple[Payment]]:
        return (
            select(Payment)
            .join(Application, Payment.application_id == Application.application_id)
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
            .order_by(Payment.payment_date.desc())
        )

    def documents(self, institution_id: object) -> Select[tuple[Document]]:
        return (
            select(Document)
            .join(Application, Document.application_id == Application.application_id)
            .join(Student, Application.student_id == Student.student_id)
            .where(Student.institution_id == institution_id)
            .order_by(Document.uploaded_at.desc())
        )

    def students(self, institution_id: object) -> Select[tuple[Student]]:
        return select(Student).where(Student.institution_id == institution_id).order_by(Student.created_at.desc())

    def fetch(self, db: Session, statement: Select[tuple[object]]) -> Sequence[object]:
        return db.scalars(statement).all()
