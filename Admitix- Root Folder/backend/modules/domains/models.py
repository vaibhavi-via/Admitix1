"""ORM model for the `domains` table (academic/professional fields
that institutions belong to, e.g. Engineering, Medical, Law, Pharmacy)."""

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
    from modules.institutions.models import Institution


class Domain(Base):
    """Academic/professional domain catalogue (Engineering, Medical,
    Law, Pharmacy, ...). Institutions belong to exactly one domain."""

    __tablename__ = "domains"

    domain_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    domain_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    domain_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    institutions: Mapped[List["Institution"]] = relationship(
        "Institution", back_populates="domain", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"<Domain domain_id={self.domain_id} domain_code={self.domain_code!r}>"
