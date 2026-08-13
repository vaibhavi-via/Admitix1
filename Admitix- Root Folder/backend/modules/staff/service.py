from __future__ import annotations

import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import Staff
from .schema import StaffCreate, StaffUpdate


def get_staff_by_id(db: Session, staff_id: uuid.UUID) -> Staff:
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff member not found.")
    return staff


def create_staff(db: Session, staff_data: StaffCreate) -> Staff:
    if db.query(Staff).filter(Staff.user_id == staff_data.user_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A staff profile already exists for this user.")
    if db.query(Staff).filter(Staff.institution_id == staff_data.institution_id, Staff.employee_id == staff_data.employee_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee ID already exists for this institution.")
    staff = Staff(**staff_data.model_dump())
    db.add(staff); db.commit(); db.refresh(staff)
    return staff


def get_staff(db: Session) -> list[Staff]:
    return db.query(Staff).order_by(Staff.employee_id).all()


def update_staff(db: Session, staff_id: uuid.UUID, staff_data: StaffUpdate) -> Staff:
    staff = get_staff_by_id(db, staff_id)
    for field, value in staff_data.model_dump(exclude_unset=True).items():
        setattr(staff, field, value)
    db.commit(); db.refresh(staff)
    return staff


def delete_staff(db: Session, staff_id: uuid.UUID) -> None:
    db.delete(get_staff_by_id(db, staff_id)); db.commit()
