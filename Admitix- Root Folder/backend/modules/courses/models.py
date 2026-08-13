"""ORM models for the `courses` module.

Houses `Course` plus the two tables that hang directly off a course:
`FeeStructure` (fee_structure) and `SeatMatrix` (seat_matrix). Grouped
here because there is no dedicated module for them and both are
course-scoped configuration, not their own top-level domain concept.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Computed,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.applications.models import ApplicationPreference
    from modules.departments.models import Department
    from modules.institutions.models import Institution
    from modules.payments.models import Payment


class Course(Base):
    """A course/program offered by a department."""

    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint(
            "institution_id", "course_code", name="uq_courses_institution_code"
        ),
        CheckConstraint("duration_years > 0", name="ck_courses_duration_years"),
        CheckConstraint("total_seats >= 0", name="ck_courses_total_seats"),
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.department_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    course_name: Mapped[str] = mapped_column(String(150), nullable=False)
    course_code: Mapped[str] = mapped_column(String(30), nullable=False)
    duration_years: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    eligibility: Mapped[str | None] = mapped_column(Text, nullable=True)
    # NOTE: kept in sync automatically with SUM(seat_matrix.total_seats)
    # for this course via a DB trigger (`trg_sync_course_total_seats`).
    # The application layer should treat this as read-only; write
    # seat counts through `SeatMatrix` instead.
    total_seats: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    department: Mapped["Department"] = relationship(
        "Department", back_populates="courses"
    )
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="courses"
    )
    fee_structures: Mapped[List["FeeStructure"]] = relationship(
        "FeeStructure", back_populates="course", cascade="all, delete-orphan"
    )
    seat_matrix_entries: Mapped[List["SeatMatrix"]] = relationship(
        "SeatMatrix", back_populates="course", cascade="all, delete-orphan"
    )
    application_preferences: Mapped[List["ApplicationPreference"]] = relationship(
        "ApplicationPreference", back_populates="course", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Course course_id={self.course_id} course_code={self.course_code!r}>"


class FeeStructure(Base):
    """Fee schedule for a course, scoped by admission category and the
    date from which it applies."""

    __tablename__ = "fee_structure"
    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "category",
            "effective_from",
            name="uq_fee_structure_course_cat_date",
        ),
        CheckConstraint("tuition_fee >= 0", name="ck_fee_structure_tuition_fee"),
        CheckConstraint("admission_fee >= 0", name="ck_fee_structure_admission_fee"),
        CheckConstraint("other_fee >= 0", name="ck_fee_structure_other_fee"),
    )

    fee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    tuition_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, server_default="0"
    )
    admission_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, server_default="0"
    )
    other_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, server_default="0"
    )
    # Database-computed generated column: tuition_fee + admission_fee + other_fee.
    total_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        Computed("tuition_fee + admission_fee + other_fee", persisted=True),
    )
    effective_from: Mapped[date] = mapped_column(nullable=False)

    # -- relationships ----------------------------------------------------
    course: Mapped["Course"] = relationship("Course", back_populates="fee_structures")
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="fee_structure", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<FeeStructure fee_id={self.fee_id} course_id={self.course_id}>"


class SeatMatrix(Base):
    """Seat allocation matrix for a course, split by admission category."""

    __tablename__ = "seat_matrix"
    __table_args__ = (
        UniqueConstraint(
            "course_id", "category", name="uq_seat_matrix_course_category"
        ),
        CheckConstraint("total_seats >= 0", name="ck_seat_matrix_total_seats"),
        CheckConstraint("filled_seats >= 0", name="ck_seat_matrix_filled_seats"),
        CheckConstraint(
            "filled_seats <= total_seats",
            name="ck_seat_matrix_filled_within_total",
        ),
    )

    seat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    filled_seats: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    # Database-computed generated column: total_seats - filled_seats.
    available_seats: Mapped[int] = mapped_column(
        Integer,
        Computed("total_seats - filled_seats", persisted=True),
    )

    # -- relationships ----------------------------------------------------
    course: Mapped["Course"] = relationship(
        "Course", back_populates="seat_matrix_entries"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<SeatMatrix seat_id={self.seat_id} course_id={self.course_id}>"
