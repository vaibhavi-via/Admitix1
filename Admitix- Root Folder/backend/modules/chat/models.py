"""ORM model for the `chat_history` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base

if TYPE_CHECKING:
    from modules.students.models import Student


class ChatHistory(Base):
    """A single question/response turn in a student's AI assistant chat
    (e.g. admission FAQ / status queries)."""

    __tablename__ = "chat_history"

    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.student_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    student: Mapped["Student"] = relationship(
        "Student", back_populates="chat_history"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ChatHistory chat_id={self.chat_id} student_id={self.student_id}>"
