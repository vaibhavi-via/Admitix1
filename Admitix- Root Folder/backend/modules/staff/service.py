from __future__ import annotations

import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import hash_password
from modules.auth.service import create_staff_activation_token
from modules.institutions.models import Institution
from modules.roles.models import Role
from modules.users.models import User, Staff
from .schema import StaffAccountCreate, StaffCreate, StaffUpdate

PLACEHOLDER_PASSWORD = "!PendingActivation!9x"


def get_staff_by_id(db: Session, staff_id: uuid.UUID) -> Staff:
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff member not found.")
    return staff


def create_staff(db: Session, staff_data: StaffCreate) -> Staff:
    if db.query(User).filter(User.user_id == staff_data.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User account not found.")
    if db.query(Staff).filter(Staff.user_id == staff_data.user_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A staff profile already exists for this user.")
    if db.query(Staff).filter(Staff.institution_id == staff_data.institution_id, Staff.employee_id == staff_data.employee_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee ID already exists for this institution.")
    staff = Staff(**staff_data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def create_staff_account(db: Session, data: StaffAccountCreate) -> dict:
    institution = db.get(Institution, data.institution_id)
    if institution is None or not institution.status:
        raise HTTPException(status_code=400, detail="Institution is invalid or inactive.")

    role = db.query(Role).filter(Role.role_name == data.role_name).first()
    if role is None or role.role_name == "student":
        raise HTTPException(status_code=400, detail="Invalid staff role.")

    if db.query(User).filter(User.institution_id == data.institution_id, User.email == data.email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists for this institution.")
    if db.query(Staff).filter(Staff.institution_id == data.institution_id, Staff.employee_id == data.employee_id).first():
        raise HTTPException(status_code=409, detail="Employee ID already exists for this institution.")

    user = User(
        institution_id=data.institution_id,
        role_id=role.role_id,
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip() if data.last_name else None,
        email=str(data.email).lower(),
        phone=data.phone,
        password_hash=hash_password(PLACEHOLDER_PASSWORD),
        is_active=False,
    )
    db.add(user)
    db.flush()

    staff = Staff(
        user_id=user.user_id,
        institution_id=data.institution_id,
        department_id=data.department_id,
        employee_id=data.employee_id.strip(),
        designation=data.designation,
        joining_date=data.joining_date,
        status=False,
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)

    return {
        "staff": staff,
        "activation_token": None,
        "activation_expires_in_hours": 48,
    }


def get_staff(db: Session) -> list[Staff]:
    return db.query(Staff).order_by(Staff.employee_id).all()


def update_staff(db: Session, staff_id: uuid.UUID, staff_data: StaffUpdate) -> Staff:
    staff = get_staff_by_id(db, staff_id)
    for field, value in staff_data.model_dump(exclude_unset=True).items():
        setattr(staff, field, value)
    if staff.user is not None and staff_data.status is not None:
        staff.user.is_active = bool(staff_data.status)
    db.commit()
    db.refresh(staff)
    return staff


def delete_staff(db: Session, staff_id: uuid.UUID) -> None:
    staff = get_staff_by_id(db, staff_id)
    db.delete(staff)
    db.commit()
