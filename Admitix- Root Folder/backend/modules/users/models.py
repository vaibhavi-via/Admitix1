"""ORM models for the `users` module.

Houses `User` (the login/account table, tenant-scoped) and `Staff`
(the employment-profile extension of `User` for non-student staff).
`Staff` lives here — rather than in its own module — because it is,
structurally, the same kind of "profile that extends a user account"
pattern `Student` is, and no dedicated `staff` module exists in the
project's module list.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.applications.models import Application, ApplicationStatusHistory
    from modules.audit_logs.models import AuditLog
    from modules.departments.models import Department
    from modules.documents.models import Document
    from modules.institutions.models import Institution
    from modules.notifications.models import Notification
    from modules.roles.models import Role
    from modules.students.models import Student


class User(Base):
    """Login/account record. Tenant-scoped via `institution_id`, which
    is NULL only for platform-level Super Admin users."""

    __tablename__ = "users"
    __table_args__ = (
        # FIX in source schema: replaces a single global UNIQUE(email)
        # with two partial unique indexes so the same email can be
        # reused as a login across different institutions, while still
        # being unique *within* one institution (and unique among
        # Super Admins, who have no institution).
        Index(
            "uq_users_institution_email",
            "institution_id",
            "email",
            unique=True,
            postgresql_where=text("institution_id IS NOT NULL"),
        ),
        Index(
            "uq_users_super_admin_email",
            "email",
            unique=True,
            postgresql_where=text("institution_id IS NULL"),
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    institution_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.role_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    profile_photo: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true(), index=True
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
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
    institution: Mapped["Institution | None"] = relationship(
        "Institution", back_populates="users"
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    staff_profile: Mapped["Staff | None"] = relationship(
        "Staff",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    student_profile: Mapped["Student | None"] = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    reviewed_applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="reviewer",
        foreign_keys="Application.reviewed_by",
        passive_deletes=True,
    )
    application_status_changes: Mapped[List["ApplicationStatusHistory"]] = (
        relationship(
            "ApplicationStatusHistory",
            back_populates="changed_by_user",
            foreign_keys="ApplicationStatusHistory.changed_by",
            passive_deletes=True,
        )
    )
    verified_documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="verifier",
        foreign_keys="Document.verified_by",
        passive_deletes=True,
    )
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="user", passive_deletes=True
    )

    @property
    def role_name(self) -> str | None:
        return self.role.role_name if self.role is not None else None

    @property
    def student_id(self):
        return self.student_profile.student_id if self.student_profile is not None else None

    @property
    def staff_id(self):
        return self.staff_profile.staff_id if self.staff_profile is not None else None

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User user_id={self.user_id} email={self.email!r}>"


class Staff(Base):
    """Employment profile for staff-type users (admission officers,
    department reviewers, finance officers, registrars, faculty, etc.).

    `institution_id` is duplicated from the parent `User` row for fast,
    join-free tenant filtering, and is kept consistent with it by the
    `trg_check_staff_institution` DB trigger — the application layer
    should always set it to match `user.institution_id`.
    """

    __tablename__ = "staff"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_staff_user_id"),
        UniqueConstraint(
            "institution_id", "employee_id", name="uq_staff_institution_empid"
        ),
    )

    staff_id: Mapped[uuid.UUID] = mapped_column(
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
    department_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.department_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False)
    designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    joining_date: Mapped[date | None] = mapped_column(nullable=True)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )

    # -- relationships ----------------------------------------------------
    user: Mapped["User"] = relationship("User", back_populates="staff_profile")
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="staff"
    )
    department: Mapped["Department | None"] = relationship(
        "Department",
        back_populates="staff_members",
        foreign_keys=[department_id],
    )
    headed_department: Mapped["Department | None"] = relationship(
        "Department",
        back_populates="hod",
        foreign_keys="Department.hod_staff_id",
        uselist=False,
    )
    assigned_applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="assigned_staff",
        foreign_keys="Application.assigned_staff_id",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Staff staff_id={self.staff_id} employee_id={self.employee_id!r}>"
