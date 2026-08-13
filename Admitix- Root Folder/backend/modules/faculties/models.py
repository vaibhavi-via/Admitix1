"""ORM model for the `faculties` table."""

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
    from modules.departments.models import Department
    from modules.institutions.models import Institution


class Faculty(Base):
    """A faculty (school) groups departments within an institution, e.g.
    Faculty of Engineering, Faculty of Medicine."""

    __tablename__ = "faculties"
    __table_args__ = (
        UniqueConstraint(
            "institution_id", "faculty_name", name="uq_faculties_institution_name"
        ),
    )

    faculty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    faculty_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="faculties"
    )
    departments: Mapped[List["Department"]] = relationship(
        "Department", back_populates="faculty", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Faculty faculty_id={self.faculty_id} faculty_name={self.faculty_name!r}>"
