"""ORM model for the `audit_logs` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.institutions.models import Institution
    from modules.users.models import User


class AuditLog(Base):
    """Immutable audit trail entry for a mutating action taken by a
    user. `institution_id` is nullable (Super Admin actions have no
    institution) and, when omitted, is auto-filled by the
    `trg_set_audit_log_institution` DB trigger from the acting user's
    `institution_id` — the application layer does not need to supply
    it explicitly.
    """

    __tablename__ = "audit_logs"

    log_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    institution_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.institution_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    record_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    # -- relationships ----------------------------------------------------
    user: Mapped["User | None"] = relationship("User", back_populates="audit_logs")
    institution: Mapped["Institution | None"] = relationship(
        "Institution", back_populates="audit_logs"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<AuditLog log_id={self.log_id} action={self.action!r} "
            f"table_name={self.table_name!r}>"
        )
