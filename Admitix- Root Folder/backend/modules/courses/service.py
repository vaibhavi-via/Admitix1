"""Business logic for the `courses` resource.

`FeeStructure` and `SeatMatrix` (also defined in this module's
`models.py`/`schema.py`) have no dedicated routes of their own — the
router only exposes CRUD for `Course` itself, with `total_seats` kept
in sync from `SeatMatrix` by a DB trigger. This module therefore only
implements the `Course` operations the router calls.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Course
from .schema import CourseCreate, CourseUpdate


def create_course(db: Session, course_data: CourseCreate) -> Course:
    """Create a new course within a department."""

    course = Course(**course_data.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


def get_courses(db: Session) -> list[Course]:
    """Return every course."""

    return db.query(Course).order_by(Course.course_name).all()


def get_course_by_id(db: Session, course_id: uuid.UUID) -> Course:
    """Fetch a single course by id or raise 404."""

    course = db.query(Course).filter(Course.course_id == course_id).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found."
        )

    return course


def update_course(db: Session, course_id: uuid.UUID, course_data: CourseUpdate) -> Course:
    """Partially update a course."""

    course = get_course_by_id(db, course_id)

    update_data = course_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course


def delete_course(db: Session, course_id: uuid.UUID) -> None:
    """Delete a course."""

    course = get_course_by_id(db, course_id)

    db.delete(course)
    db.commit()

# ---------------------------------------------------------------------------
# Fee Structure
# ---------------------------------------------------------------------------

def create_fee_structure(db: Session, fee_data):
    from .models import FeeStructure
    fee = FeeStructure(**fee_data.model_dump())
    db.add(fee)
    db.commit()
    db.refresh(fee)
    return fee


def get_fee_structures(db: Session):
    from .models import FeeStructure
    return db.query(FeeStructure).order_by(FeeStructure.effective_from.desc()).all()


def get_fee_structure_by_id(db: Session, fee_id: uuid.UUID):
    from .models import FeeStructure
    fee = db.query(FeeStructure).filter(FeeStructure.fee_id == fee_id).first()
    if fee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fee structure not found.")
    return fee


def update_fee_structure(db: Session, fee_id: uuid.UUID, fee_data):
    fee = get_fee_structure_by_id(db, fee_id)
    for field, value in fee_data.model_dump(exclude_unset=True).items():
        setattr(fee, field, value)
    db.commit()
    db.refresh(fee)
    return fee


def delete_fee_structure(db: Session, fee_id: uuid.UUID) -> None:
    fee = get_fee_structure_by_id(db, fee_id)
    db.delete(fee)
    db.commit()


# ---------------------------------------------------------------------------
# Seat Matrix
# ---------------------------------------------------------------------------

def create_seat_matrix(db: Session, seat_data):
    from .models import SeatMatrix
    seat = SeatMatrix(**seat_data.model_dump())
    db.add(seat)
    db.commit()
    db.refresh(seat)
    return seat


def get_seat_matrix(db: Session):
    from .models import SeatMatrix
    return db.query(SeatMatrix).order_by(SeatMatrix.category).all()


def get_seat_matrix_by_id(db: Session, seat_id: uuid.UUID):
    from .models import SeatMatrix
    seat = db.query(SeatMatrix).filter(SeatMatrix.seat_id == seat_id).first()
    if seat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat matrix entry not found.")
    return seat


def update_seat_matrix(db: Session, seat_id: uuid.UUID, seat_data):
    seat = get_seat_matrix_by_id(db, seat_id)
    for field, value in seat_data.model_dump(exclude_unset=True).items():
        setattr(seat, field, value)
    db.commit()
    db.refresh(seat)
    return seat


def delete_seat_matrix(db: Session, seat_id: uuid.UUID) -> None:
    seat = get_seat_matrix_by_id(db, seat_id)
    db.delete(seat)
    db.commit()
