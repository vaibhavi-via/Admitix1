from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, require_own_student, role_name
from modules.students.models import Student
from modules.users.models import User
from .models import EducationDetail
from .schema import EducationDetailCreate, EducationDetailUpdate

def _student(db: Session, student_id: uuid.UUID, user: User) -> Student:
    student = db.get(Student, student_id)
    if student is None: raise HTTPException(status_code=404, detail="Student not found.")
    require_same_institution(user, student.institution_id); require_own_student(user, student); return student

def get_education_detail_by_id(db: Session, education_id: uuid.UUID, user: User) -> EducationDetail:
    item = db.get(EducationDetail, education_id)
    if item is None: raise HTTPException(status_code=404, detail="Educational detail not found.")
    _student(db, item.student_id, user); return item

def create_education_detail(db: Session, data: EducationDetailCreate, user: User) -> EducationDetail:
    _student(db, data.student_id, user)
    item = EducationDetail(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

def get_education_details(db: Session, student_id: uuid.UUID | None, user: User) -> list[EducationDetail]:
    if role_name(user) == "student":
        student_id = user.student_id
    query = db.query(EducationDetail)
    if student_id is not None: _student(db, student_id, user); query = query.filter(EducationDetail.student_id == student_id)
    return query.order_by(EducationDetail.created_at.desc()).all()

def update_education_detail(db: Session, education_id: uuid.UUID, data: EducationDetailUpdate, user: User) -> EducationDetail:
    item = get_education_detail_by_id(db, education_id, user)
    for field, value in data.model_dump(exclude_unset=True).items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item

def delete_education_detail(db: Session, education_id: uuid.UUID, user: User) -> None:
    item = get_education_detail_by_id(db, education_id, user)
    if role_name(user) == "student": raise HTTPException(status_code=403, detail="Students cannot delete educational details.")
    db.delete(item); db.commit()
