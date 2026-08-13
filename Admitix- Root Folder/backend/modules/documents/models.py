"""ORM model for the `documents` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import DocumentVerificationStatus
from db.base import Base

if TYPE_CHECKING:
    from modules.ai_verification.models import AIVerification
    from modules.applications.models import Application
    from modules.document_types.models import DocumentType
    from modules.users.models import User


class Document(Base):
    """A document uploaded by a student against an application (e.g.
    marksheet, ID proof)."""

    __tablename__ = "documents"

    document_id: Mapped[uuid.UUID] = mapped_column(
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
    document_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_types.document_type_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)
    verification_status: Mapped[DocumentVerificationStatus] = mapped_column(
        Enum(
            DocumentVerificationStatus,
            name="document_verification_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=DocumentVerificationStatus.PENDING.value,
        index=True,
    )
    verified_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    # -- relationships ----------------------------------------------------
    application: Mapped["Application"] = relationship(
        "Application", back_populates="documents"
    )
    document_type: Mapped["DocumentType"] = relationship(
        "DocumentType", back_populates="documents"
    )
    verifier: Mapped["User | None"] = relationship(
        "User", back_populates="verified_documents", foreign_keys=[verified_by]
    )
    ai_verification: Mapped["AIVerification | None"] = relationship(
        "AIVerification",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Document document_id={self.document_id} file_name={self.file_name!r}>"
