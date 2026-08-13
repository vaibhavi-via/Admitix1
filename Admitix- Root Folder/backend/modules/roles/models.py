"""ORM model for the `roles` table (RBAC role catalogue)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.users.models import User


class Role(Base):
    """RBAC roles: super_admin, institution_admin, admission_officer,
    department_reviewer, finance_officer, registrar, faculty, student,
    guardian."""

    __tablename__ = "roles"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="role", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"<Role role_id={self.role_id} role_name={self.role_name!r}>"
