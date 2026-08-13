"""ORM model for the `ai_verifications` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import AIVerificationStatus
from db.base import Base

if TYPE_CHECKING:
    from modules.documents.models import Document


class AIVerification(Base):
    """AI-assisted (OCR + heuristic) verification result for a single
    document. One-to-one with `Document`.

    A human verifier can still manually override the parent
    `documents.verification_status` afterward — the
    `trg_sync_document_status` DB trigger only sets the initial
    AI-driven state (from `pending`), it never overwrites a status a
    human has already changed.
    """

    __tablename__ = "ai_verifications"
    __table_args__ = (
        UniqueConstraint("document_id", name="uq_ai_verifications_document_id"),
        CheckConstraint(
            "confidence_score BETWEEN 0 AND 100",
            name="ck_ai_verifications_confidence_score",
        ),
        CheckConstraint(
            "blur_score BETWEEN 0 AND 100", name="ck_ai_verifications_blur_score"
        ),
    )

    verification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.document_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ocr_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    blur_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    missing_fields: Mapped[str | None] = mapped_column(Text, nullable=True)
    name_match: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    status: Mapped[AIVerificationStatus] = mapped_column(
        Enum(
            AIVerificationStatus,
            name="ai_verification_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=AIVerificationStatus.PENDING.value,
    )
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # -- relationships ----------------------------------------------------
    document: Mapped["Document"] = relationship(
        "Document", back_populates="ai_verification"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AIVerification verification_id={self.verification_id} status={self.status}>"
