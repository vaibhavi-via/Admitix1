"""Business logic for the `students` resource.

`EducationDetail` and `EntranceExamScore` (also defined in this
module's `models.py`/`schema.py`) have no dedicated routes of their
own — the router only exposes CRUD for `Student` itself. This module
therefore only implements the `Student` operations the router calls.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Student
from .schema import StudentCreate, StudentUpdate


def create_student(db: Session, student_data: StudentCreate) -> Student:
    """Create a new student profile extending an existing user
    account."""

    existing = db.query(Student).filter(Student.user_id == student_data.user_id).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student profile already exists for this user.",
        )

    student = Student(**student_data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_students(db: Session) -> list[Student]:
    """Return every student."""

    return db.query(Student).order_by(Student.created_at.desc()).all()


def get_student_by_id(db: Session, student_id: uuid.UUID) -> Student:
    """Fetch a single student by id or raise 404."""

    student = db.query(Student).filter(Student.student_id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found."
        )

    return student


def update_student(db: Session, student_id: uuid.UUID, student_data: StudentUpdate) -> Student:
    """Partially update a student profile."""

    student = get_student_by_id(db, student_id)

    update_data = student_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: uuid.UUID) -> None:
    """Delete a student profile (cascades to education details,
    entrance exam scores, applications, and chat history per the
    model's relationship config)."""

    student = get_student_by_id(db, student_id)

    db.delete(student)
    db.commit()
