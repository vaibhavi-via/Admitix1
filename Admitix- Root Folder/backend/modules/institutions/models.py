"""ORM model for the `institutions` table (multi-tenant root entity)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.admission_cycles.models import AdmissionCycle
    from modules.applications.models import ApplicationStatusHistory
    from modules.audit_logs.models import AuditLog
    from modules.courses.models import Course
    from modules.departments.models import Department
    from modules.faculties.models import Faculty
    from modules.students.models import Student
    from modules.users.models import Staff, User


class Institution(Base):
    """Tenant institutions (colleges) onboarded onto the platform."""

    __tablename__ = "institutions"

    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    institution_name: Mapped[str] = mapped_column(String(150), nullable=False)
    institution_code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="India"
    )
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # -- relationships ----------------------------------------------------
    faculties: Mapped[List["Faculty"]] = relationship(
        "Faculty", back_populates="institution", passive_deletes=True
    )
    departments: Mapped[List["Department"]] = relationship(
        "Department", back_populates="institution", passive_deletes=True
    )
    courses: Mapped[List["Course"]] = relationship(
        "Course", back_populates="institution", passive_deletes=True
    )
    admission_cycles: Mapped[List["AdmissionCycle"]] = relationship(
        "AdmissionCycle", back_populates="institution", passive_deletes=True
    )
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="institution", passive_deletes=True
    )
    staff: Mapped[List["Staff"]] = relationship(
        "Staff", back_populates="institution", passive_deletes=True
    )
    students: Mapped[List["Student"]] = relationship(
        "Student", back_populates="institution", passive_deletes=True
    )
    application_status_history: Mapped[List["ApplicationStatusHistory"]] = (
        relationship(
            "ApplicationStatusHistory",
            back_populates="institution",
            passive_deletes=True,
        )
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="institution", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Institution institution_id={self.institution_id} "
            f"institution_code={self.institution_code!r}>"
        )
