"""ORM model for the `notifications` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import NotificationType
from db.base import Base

if TYPE_CHECKING:
    from modules.users.models import User


class Notification(Base):
    """An in-app/email/SMS notification sent to a user."""

    __tablename__ = "notifications"
    __table_args__ = (
        Index("idx_notifications_is_read", "user_id", "is_read"),
    )

    notification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(
            NotificationType,
            name="notification_type",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=NotificationType.IN_APP.value,
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=func.false()
    )
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Notification notification_id={self.notification_id} user_id={self.user_id}>"
