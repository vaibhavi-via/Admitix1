"""ORM model for the `admission_cycles` table."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import AdmissionCycleStatus
from db.base import Base

if TYPE_CHECKING:
    from modules.applications.models import Application
    from modules.institutions.models import Institution


class AdmissionCycle(Base):
    """An admission cycle/intake window (e.g. academic year 2026-27)
    for an institution."""

    __tablename__ = "admission_cycles"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "academic_year",
            name="uq_admission_cycles_institution_year",
        ),
        CheckConstraint(
            "application_end > application_start",
            name="ck_admission_cycles_dates",
        ),
    )

    cycle_id: Mapped[uuid.UUID] = mapped_column(
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
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    application_start: Mapped[date] = mapped_column(nullable=False)
    application_end: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[AdmissionCycleStatus] = mapped_column(
        Enum(
            AdmissionCycleStatus,
            name="admission_cycle_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=AdmissionCycleStatus.UPCOMING.value,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    institution: Mapped["Institution"] = relationship(
        "Institution", back_populates="admission_cycles"
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application", back_populates="cycle", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<AdmissionCycle cycle_id={self.cycle_id} "
            f"academic_year={self.academic_year!r}>"
        )
