"""ORM models for the `applications` module.

Houses `Application` plus `ApplicationPreference` (course preference
ordering per application) and `ApplicationStatusHistory` (status audit
trail) — both are application-scoped and have no dedicated module.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import ApplicationCurrentStatus, PreferenceStatus
from db.base import Base

if TYPE_CHECKING:
    from modules.admission_cycles.models import AdmissionCycle
    from modules.courses.models import Course
    from modules.documents.models import Document
    from modules.institutions.models import Institution
    from modules.payments.models import Payment
    from modules.students.models import Student
    from modules.users.models import User, Staff


class Application(Base):
    """A student's admission application within a specific admission
    cycle. A student may have at most one application per cycle."""

    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("application_number", name="uq_applications_number"),
        UniqueConstraint(
            "student_id", "cycle_id", name="uq_applications_student_cycle"
        ),
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
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
    cycle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("admission_cycles.cycle_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    application_number: Mapped[str] = mapped_column(String(30), nullable=False)
    submission_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    current_status: Mapped[ApplicationCurrentStatus] = mapped_column(
        Enum(
            ApplicationCurrentStatus,
            name="application_current_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=ApplicationCurrentStatus.DRAFT.value,
        index=True,
    )
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    assigned_staff_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staff.staff_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    student: Mapped["Student"] = relationship("Student", back_populates="applications")
    cycle: Mapped["AdmissionCycle"] = relationship(
        "AdmissionCycle", back_populates="applications"
    )
    reviewer: Mapped["User | None"] = relationship(
        "User", back_populates="reviewed_applications", foreign_keys=[reviewed_by]
    )
    assigned_staff: Mapped["Staff | None"] = relationship(
        "Staff", back_populates="assigned_applications", foreign_keys=[assigned_staff_id]
    )
    preferences: Mapped[List["ApplicationPreference"]] = relationship(
        "ApplicationPreference", back_populates="application", cascade="all, delete-orphan"
    )
    status_history: Mapped[List["ApplicationStatusHistory"]] = relationship(
        "ApplicationStatusHistory",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document", back_populates="application", cascade="all, delete-orphan"
    )
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="application", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Application application_id={self.application_id} "
            f"application_number={self.application_number!r}>"
        )


class ApplicationPreference(Base):
    """Ordered course preference for an application (preference 1, 2,
    3, ...). At most one preference per application may be
    `allotted` — enforced by a partial unique index
    (`uq_app_preferences_one_allotted`) — and `filled_seats` on the
    matching `SeatMatrix` row is kept in sync automatically by a DB
    trigger when a preference becomes/un-becomes `allotted`.
    """

    __tablename__ = "application_preferences"
    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "preference_no",
            name="uq_app_preferences_app_order",
        ),
        UniqueConstraint(
            "application_id", "course_id", name="uq_app_preferences_app_course"
        ),
        Index(
            "uq_app_preferences_one_allotted",
            "application_id",
            unique=True,
            postgresql_where=text("status = 'allotted'"),
        ),
    )

    preference_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.application_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.course_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    preference_no: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    status: Mapped[PreferenceStatus] = mapped_column(
        Enum(
            PreferenceStatus,
            name="application_preference_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=PreferenceStatus.PENDING.value,
    )

    # -- relationships ----------------------------------------------------
    application: Mapped["Application"] = relationship(
        "Application", back_populates="preferences"
    )
    course: Mapped["Course"] = relationship(
        "Course", back_populates="application_preferences"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<ApplicationPreference preference_id={self.preference_id} "
            f"preference_no={self.preference_no}>"
        )


class ApplicationStatusHistory(Base):
    """Immutable audit trail of `current_status` transitions for an
    application. `institution_id` is auto-filled by a DB trigger
    (`trg_set_status_history_institution`) when not supplied, so it can
    be filtered on directly without joining through
    applications -> students."""

    __tablename__ = "application_status_history"

    history_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.application_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    old_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    new_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    application: Mapped["Application"] = relationship(
        "Application", back_populates="status_history"
    )
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="application_status_history"
    )
    changed_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="application_status_changes",
        foreign_keys=[changed_by],
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ApplicationStatusHistory history_id={self.history_id}>"
