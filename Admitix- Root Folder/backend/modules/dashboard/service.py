"""Role-aware dashboard aggregations."""
from __future__ import annotations
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.enums import ApplicationCurrentStatus, DocumentVerificationStatus, PaymentStatus
from core.authorization import role_name
from modules.applications.models import Application
from modules.courses.models import Course, SeatMatrix
from modules.documents.models import Document
from modules.payments.models import Payment
from modules.students.models import Student
from modules.users.models import Staff


def _application_scope(db: Session, current_user):
    q = db.query(Application).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: q = q.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        if staff is None: return q.filter(False)
        q = q.filter(Application.assigned_staff_id == staff.staff_id)
    return q


def get_dashboard_summary(db: Session, current_user) -> dict:
    applications = _application_scope(db, current_user).subquery()
    total_applications = db.query(func.count(applications.c.application_id)).scalar() or 0
    total_admitted = db.query(func.count(applications.c.application_id)).filter(applications.c.current_status == ApplicationCurrentStatus.ADMITTED.value).scalar() or 0
    payments = db.query(Payment).join(Application, Payment.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: payments = payments.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        payments = payments.filter(Application.assigned_staff_id == staff.staff_id) if staff else payments.filter(False)
    total_revenue_collected = payments.filter(Payment.payment_status == PaymentStatus.SUCCESS).with_entities(func.coalesce(func.sum(Payment.amount_paid), 0)).scalar() or 0
    docs = db.query(Document).join(Application, Document.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: docs = docs.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        docs = docs.filter(Application.assigned_staff_id == staff.staff_id) if staff else docs.filter(False)
    pending_docs = docs.filter(Document.verification_status == DocumentVerificationStatus.PENDING).count()
    return {"total_applications": total_applications, "total_admitted": total_admitted, "total_revenue_collected": float(total_revenue_collected), "pending_document_verifications": pending_docs}


def get_admission_statistics(db: Session, current_user):
    rows = _application_scope(db, current_user).with_entities(Application.cycle_id, Application.current_status, func.count(Application.application_id)).group_by(Application.cycle_id, Application.current_status).all()
    funnels = {}
    for cycle_id, current_status, count in rows:
        funnel = funnels.setdefault(cycle_id, {status.value: 0 for status in ApplicationCurrentStatus} | {"cycle_id": cycle_id})
        funnel[current_status.value] = count
    return list(funnels.values())


def get_recent_applications(db: Session, current_user, limit: int = 10):
    return _application_scope(db, current_user).order_by(Application.submission_date.desc()).limit(limit).all()


def get_payment_summary(db: Session, current_user):
    rows = db.query(Payment.payment_status, func.count(Payment.payment_id), func.coalesce(func.sum(Payment.amount_paid), 0)).join(Application, Payment.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: rows = rows.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        rows = rows.filter(Application.assigned_staff_id == staff.staff_id) if staff else rows.filter(False)
    rows = rows.group_by(Payment.payment_status).all()
    return {status.value: {"count": 0, "total_amount": 0.0} for status in PaymentStatus} | {s.value: {"count": c, "total_amount": float(a)} for s,c,a in rows}


def get_document_statistics(db: Session, current_user):
    rows = db.query(Document.verification_status, func.count(Document.document_id)).join(Application, Document.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: rows = rows.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == current_user.user_id).first()
        rows = rows.filter(Application.assigned_staff_id == staff.staff_id) if staff else rows.filter(False)
    rows = rows.group_by(Document.verification_status).all()
    return {status.value: 0 for status in DocumentVerificationStatus} | {s.value: c for s,c in rows}


def get_seat_occupancy(db: Session, current_user):
    rows = db.query(Course.course_id, Course.course_name, func.coalesce(func.sum(SeatMatrix.total_seats),0), func.coalesce(func.sum(SeatMatrix.filled_seats),0)).outerjoin(SeatMatrix, SeatMatrix.course_id == Course.course_id).group_by(Course.course_id, Course.course_name).all()
    return [{"course_id": cid, "course_name": name, "total_seats": total, "filled_seats": filled, "available_seats": total-filled} for cid,name,total,filled in rows]
