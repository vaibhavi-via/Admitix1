from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, require_own_student, role_name
from modules.users.models import User
from .models import Student
from .schema import StudentCreate, StudentUpdate


def create_student(db: Session, student_data: StudentCreate, current_user: User) -> Student:
    require_same_institution(current_user, student_data.institution_id)
    if role_name(current_user) == "student" and student_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own student profile.")
    existing = db.query(Student).filter(Student.user_id == student_data.user_id).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="A student profile already exists for this user.")
    student = Student(**student_data.model_dump())
    db.add(student); db.commit(); db.refresh(student); return student


def get_students(db: Session, current_user: User) -> list[Student]:
    query = db.query(Student)
    if current_user.institution_id is not None:
        query = query.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "student":
        query = query.filter(Student.user_id == current_user.user_id)
    return query.order_by(Student.created_at.desc()).all()


def get_student_by_id(db: Session, student_id: uuid.UUID, current_user: User) -> Student:
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    require_same_institution(current_user, student.institution_id)
    require_own_student(current_user, student)
    return student


def update_student(db: Session, student_id: uuid.UUID, student_data: StudentUpdate, current_user: User) -> Student:
    student = get_student_by_id(db, student_id, current_user)
    for field, value in student_data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit(); db.refresh(student); return student


def delete_student(db: Session, student_id: uuid.UUID, current_user: User) -> None:
    student = get_student_by_id(db, student_id, current_user)
    if role_name(current_user) == "student":
        raise HTTPException(status_code=403, detail="Students cannot delete their profile.")
    db.delete(student); db.commit()
