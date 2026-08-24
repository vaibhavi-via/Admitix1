from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, require_own_student, role_name
from modules.applications.models import Application
from modules.students.models import Student
from modules.users.models import Staff, User
from .models import Payment
from .schema import PaymentCreate, PaymentUpdate

def _application(db: Session, application_id: uuid.UUID, user: User) -> Application:
    app = db.get(Application, application_id)
    if app is None: raise HTTPException(status_code=404, detail="Application not found.")
    student = db.get(Student, app.student_id)
    require_same_institution(user, student.institution_id); require_own_student(user, student)
    if role_name(user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == user.user_id).first()
        if staff is None or app.assigned_staff_id != staff.staff_id:
            raise HTTPException(status_code=403, detail="This application is not assigned to you.")
    return app

def _ensure_unique_transaction_id(db: Session, transaction_id: str | None, exclude: uuid.UUID | None = None) -> None:
    if not transaction_id: return
    q = db.query(Payment).filter(Payment.transaction_id == transaction_id)
    if exclude: q = q.filter(Payment.payment_id != exclude)
    if q.first() is not None: raise HTTPException(status_code=409, detail=f"Transaction id '{transaction_id}' has already been recorded.")

def create_payment(db: Session, payment_data: PaymentCreate, user: User) -> Payment:
    _application(db, payment_data.application_id, user)
    _ensure_unique_transaction_id(db, payment_data.transaction_id)
    payment = Payment(**payment_data.model_dump()); db.add(payment); db.commit(); db.refresh(payment); return payment

def get_payments(db: Session, user: User) -> list[Payment]:
    q = db.query(Payment).join(Application, Payment.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if user.institution_id is not None: q = q.filter(Student.institution_id == user.institution_id)
    if role_name(user) == "student":
        q = q.filter(Student.user_id == user.user_id)
    elif role_name(user) == "admission_officer":
        staff = db.query(Staff).filter(Staff.user_id == user.user_id).first()
        if staff is None: return []
        q = q.filter(Application.assigned_staff_id == staff.staff_id)
    return q.order_by(Payment.payment_date.desc()).all()

def get_payment_by_id(db: Session, payment_id: uuid.UUID, user: User) -> Payment:
    payment = db.get(Payment, payment_id)
    if payment is None: raise HTTPException(status_code=404, detail="Payment not found.")
    _application(db, payment.application_id, user); return payment

def update_payment(db: Session, payment_id: uuid.UUID, payment_data: PaymentUpdate, user: User) -> Payment:
    payment = get_payment_by_id(db, payment_id, user)
    if role_name(user) == "student":
        raise HTTPException(status_code=403, detail="Students can view payments but cannot modify payment records.")
    updates = payment_data.model_dump(exclude_unset=True)
    if "transaction_id" in updates: _ensure_unique_transaction_id(db, updates["transaction_id"], payment_id)
    for field, value in updates.items(): setattr(payment, field, value)
    db.commit(); db.refresh(payment); return payment

def delete_payment(db: Session, payment_id: uuid.UUID, user: User) -> None:
    payment = get_payment_by_id(db, payment_id, user)
    if role_name(user) != "institution_admin" and role_name(user) != "super_admin":
        raise HTTPException(status_code=403, detail="Only administrators can delete payments.")
    db.delete(payment); db.commit()
