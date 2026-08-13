"""ORM model for the `document_types` table (global lookup)."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.documents.models import Document


class DocumentType(Base):
    """Global catalogue of document types (e.g. 10th marksheet, Aadhaar
    card, migration certificate). Not per-institution/per-course by
    design — see closing note in `final_schema_sql.sql`."""

    __tablename__ = "document_types"

    document_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    document_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    mandatory: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.true()
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # -- relationships ----------------------------------------------------
    documents: Mapped[List["Document"]] = relationship(
        "Document", back_populates="document_type", passive_deletes=True
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<DocumentType document_type_id={self.document_type_id} "
            f"document_name={self.document_name!r}>"
        )
