"""Business logic for the `reports` module.

Read-only report generation composed from other modules' ORM models
(`Application`, `Student`, `User`, `Payment`, `Document`). No dedicated
table backs this module. The router currently calls each `generate_*`
function with only a `db` session (no filters/date-range yet — see
`AdmittedStudentsReportRequest` / `FeeCollectionReportRequest` in
`schema.py` for the filters a future version of these endpoints could
accept as query parameters), so each function here returns an
unfiltered, tenant-wide report.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from core.enums import ApplicationCurrentStatus, DocumentVerificationStatus, PaymentStatus
from modules.applications.models import Application
from modules.documents.models import Document
from modules.payments.models import Payment
from modules.students.models import Student
from modules.users.models import User, Staff


def generate_admission_report(db: Session, current_user) -> list[dict]:
    query = (db.query(Application.application_id, Application.application_number, Application.cycle_id, Application.current_status, User.first_name, User.last_name)
        .join(Student, Application.student_id == Student.student_id)
        .join(User, Student.user_id == User.user_id))
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if getattr(current_user, "role_name", None) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        query = query.filter(Application.assigned_staff_id == staff.staff_id) if staff else query.filter(False)
    rows = query.order_by(Application.submission_date.desc()).all()
    return [{"application_id": application_id, "application_number": application_number, "cycle_id": cycle_id, "current_status": current_status.value, "student_name": " ".join(filter(None, [first_name, last_name]))} for application_id, application_number, cycle_id, current_status, first_name, last_name in rows]


def generate_payment_report(db: Session, current_user) -> list[dict]:
    query = (db.query(Payment.payment_id, Payment.application_id, Payment.amount_paid, Payment.payment_status, Payment.payment_mode, Payment.payment_date)
        .join(Application, Payment.application_id == Application.application_id)
        .join(Student, Application.student_id == Student.student_id))
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if getattr(current_user, "role_name", None) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        query = query.filter(Application.assigned_staff_id == staff.staff_id) if staff else query.filter(False)
    rows = query.order_by(Payment.payment_date.desc()).all()
    return [{"payment_id": pid, "application_id": aid, "amount_paid": float(amount), "payment_status": status.value, "payment_mode": mode.value if mode else None, "payment_date": payment_date.isoformat()} for pid,aid,amount,status,mode,payment_date in rows]

def generate_document_report(db: Session, current_user) -> list[dict]:
    query = db.query(Document.verification_status, func.count(Document.document_id)).join(Application, Document.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if getattr(current_user, "role_name", None) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        query = query.filter(Application.assigned_staff_id == staff.staff_id) if staff else query.filter(False)
    rows = query.group_by(Document.verification_status).all()
    report = {status.value: 0 for status in DocumentVerificationStatus}
    for verification_status, count in rows: report[verification_status.value] = count
    return [{"verification_status": k, "count": v} for k,v in report.items()]

def generate_student_report(db: Session, current_user) -> list[dict]:
    query = db.query(Student.student_id, User.first_name, User.last_name, User.email).join(User, Student.user_id == User.user_id)
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if getattr(current_user, "role_name", None) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        query = query.join(Application, Application.student_id == Student.student_id).filter(Application.assigned_staff_id == staff.staff_id) if staff else query.filter(False)
    rows = query.order_by(User.first_name).all()
    return [{"student_id": sid, "student_name": " ".join(filter(None, [first_name, last_name])), "email": email} for sid,first_name,last_name,email in rows]


def export_report(db: Session, current_user) -> dict:
    """Placeholder export endpoint.

    A real implementation would take a `ReportFormat` (csv/xlsx/pdf)
    and a report type, render the corresponding `generate_*` rows to
    that file format, persist it to storage, and return a
    `ReportGeneratedResponse`-shaped payload. Since the router does not
    yet pass those parameters, this returns a stub response.
    """

    return {
        "file_name": "report-export-placeholder.csv",
        "file_url": "",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "detail": (
            "Export requires a report type and format; wire "
            "AdmittedStudentsReportRequest/FeeCollectionReportRequest "
            "as query parameters on this route to enable a real export."
        ),
    }
