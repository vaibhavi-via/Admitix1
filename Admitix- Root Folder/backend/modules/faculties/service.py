"""Business logic for the `faculties` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Faculty
from .schema import FacultyCreate, FacultyUpdate


def create_faculty(db: Session, faculty_data: FacultyCreate) -> Faculty:
    """Create a new faculty within an institution."""

    faculty = Faculty(**faculty_data.model_dump())

    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    return faculty


def get_faculties(db: Session) -> list[Faculty]:
    """Return every faculty."""

    return db.query(Faculty).order_by(Faculty.faculty_name).all()


def get_faculty_by_id(db: Session, faculty_id: uuid.UUID) -> Faculty:
    """Fetch a single faculty by id or raise 404."""

    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()

    if faculty is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found."
        )

    return faculty


def update_faculty(db: Session, faculty_id: uuid.UUID, faculty_data: FacultyUpdate) -> Faculty:
    """Partially update a faculty."""

    faculty = get_faculty_by_id(db, faculty_id)

    update_data = faculty_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faculty, field, value)

    db.commit()
    db.refresh(faculty)

    return faculty


def delete_faculty(db: Session, faculty_id: uuid.UUID) -> None:
    """Delete a faculty."""

    faculty = get_faculty_by_id(db, faculty_id)

    db.delete(faculty)
    db.commit()
