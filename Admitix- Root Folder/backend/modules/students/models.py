"""ORM models for the `students` module.

Houses `Student` plus the two profile-detail tables that hang off a
student and have no dedicated module of their own: `EducationDetail`
(education_details) and `EntranceExamScore` (entrance_exam_scores).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import Gender
from db.base import Base

if TYPE_CHECKING:
    from modules.applications.models import Application
    from modules.chat.models import ChatHistory
    from modules.institutions.models import Institution
    from modules.users.models import User


class Student(Base):
    """Student profile, extending a `User` account.

    `institution_id` is duplicated from the parent `User` row for
    fast, join-free tenant filtering, and is kept consistent with it
    by the `trg_check_student_institution` DB trigger.
    """

    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_students_user_id"),
        Index(
            "uq_students_institution_aadhaar",
            "institution_id",
            "aadhaar_no",
            unique=True,
            postgresql_where=text("aadhaar_no IS NOT NULL"),
        ),
        CheckConstraint(
            "gender IN ('male', 'female', 'other', 'prefer_not_to_say')",
            name="ck_students_gender",
        ),
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    aadhaar_no: Mapped[str | None] = mapped_column(String(20), nullable=True)
    gender: Mapped[Gender | None] = mapped_column(
        Enum(
            Gender,
            name="student_gender",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=True,
    )
    dob: Mapped[date | None] = mapped_column(nullable=True)
    blood_group: Mapped[str | None] = mapped_column(String(5), nullable=True)
    category: Mapped[str | None] = mapped_column(String(30), nullable=True)
    nationality: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="Indian"
    )
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    parent_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    parent_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    guardian_email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    user: Mapped["User"] = relationship("User", back_populates="student_profile")
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="students"
    )
    education_details: Mapped[List["EducationDetail"]] = relationship(
        "EducationDetail", back_populates="student", cascade="all, delete-orphan"
    )
    entrance_exam_scores: Mapped[List["EntranceExamScore"]] = relationship(
        "EntranceExamScore", back_populates="student", cascade="all, delete-orphan"
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application", back_populates="student", cascade="all, delete-orphan"
    )
    chat_history: Mapped[List["ChatHistory"]] = relationship(
        "ChatHistory", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Student student_id={self.student_id} user_id={self.user_id}>"


class EducationDetail(Base):
    """Prior academic qualification record for a student (10th, 12th,
    diploma, degree, etc.)."""

    __tablename__ = "education_details"
    __table_args__ = (
        CheckConstraint(
            "passing_year BETWEEN 1950 AND 2100",
            name="ck_education_details_passing_year",
        ),
        CheckConstraint(
            "percentage BETWEEN 0 AND 100",
            name="ck_education_details_percentage",
        ),
        CheckConstraint("cgpa BETWEEN 0 AND 10", name="ck_education_details_cgpa"),
    )

    education_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    qualification: Mapped[str] = mapped_column(String(100), nullable=False)
    board_university: Mapped[str | None] = mapped_column(String(150), nullable=True)
    institution_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    passing_year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    seat_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    cgpa: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    student: Mapped["Student"] = relationship(
        "Student", back_populates="education_details"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<EducationDetail education_id={self.education_id} "
            f"student_id={self.student_id}>"
        )


class EntranceExamScore(Base):
    """Entrance exam score record for a student (JEE, NEET, CET, etc.)."""

    __tablename__ = "entrance_exam_scores"
    __table_args__ = (
        CheckConstraint(
            "percentile BETWEEN 0 AND 100",
            name="ck_entrance_exam_scores_percentile",
        ),
        CheckConstraint("rank > 0", name="ck_entrance_exam_scores_rank"),
        CheckConstraint(
            "exam_year BETWEEN 1950 AND 2100",
            name="ck_entrance_exam_scores_exam_year",
        ),
    )

    score_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exam_name: Mapped[str] = mapped_column(String(100), nullable=False)
    roll_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    score: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    percentile: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    exam_year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    student: Mapped["Student"] = relationship(
        "Student", back_populates="entrance_exam_scores"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<EntranceExamScore score_id={self.score_id} student_id={self.student_id}>"
