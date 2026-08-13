"""ORM model for the `departments` table.

Note: `hod_staff_id` -> `staff.staff_id` is a genuinely circular FK in
the SQL schema (added via a deferred `ALTER TABLE ... ADD CONSTRAINT`
after `staff` exists, see section 8.1 of `final_schema_sql.sql`,
because `staff.department_id` already points back at `departments`).
`use_alter=True` reproduces that exact deferred-constraint behaviour
so Alembic/DDL creation order does not deadlock on the cycle.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.courses.models import Course
    from modules.faculties.models import Faculty
    from modules.institutions.models import Institution
    from modules.users.models import Staff


class Department(Base):
    """Academic department belonging to a faculty."""

    __tablename__ = "departments"
    __table_args__ = (
        UniqueConstraint(
            "faculty_id", "department_name", name="uq_departments_faculty_name"
        ),
    )

    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    faculty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("faculties.faculty_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    department_name: Mapped[str] = mapped_column(String(150), nullable=False)
    hod_staff_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "staff.staff_id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_departments_hod_staff",
        ),
        nullable=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    faculty: Mapped["Faculty"] = relationship("Faculty", back_populates="departments")
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="departments"
    )
    hod: Mapped["Staff | None"] = relationship(
        "Staff",
        foreign_keys=[hod_staff_id],
        back_populates="headed_department",
        post_update=True,
    )
    staff_members: Mapped[List["Staff"]] = relationship(
        "Staff",
        back_populates="department",
        foreign_keys="Staff.department_id",
        passive_deletes=True,
    )
    courses: Mapped[List["Course"]] = relationship(
        "Course", back_populates="department", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Department department_id={self.department_id} "
            f"department_name={self.department_name!r}>"
        )
