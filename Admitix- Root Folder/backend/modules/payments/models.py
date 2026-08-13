"""ORM model for the `payments` table."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.enums import PaymentMode, PaymentStatus
from db.base import Base

if TYPE_CHECKING:
    from modules.applications.models import Application
    from modules.courses.models import FeeStructure


class Payment(Base):
    """A fee payment made against an application."""

    __tablename__ = "payments"
    __table_args__ = (
        UniqueConstraint(
            "transaction_id", name="uq_payments_transaction_id"
        ),
        CheckConstraint("amount_paid > 0", name="ck_payments_amount_paid"),
    )

    payment_id: Mapped[uuid.UUID] = mapped_column(
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
    fee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fee_structure.fee_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_mode: Mapped[PaymentMode | None] = mapped_column(
        Enum(
            PaymentMode,
            name="payment_mode",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=True,
    )
    transaction_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            name="payment_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        server_default=PaymentStatus.PENDING.value,
        index=True,
    )
    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # -- relationships ----------------------------------------------------
    application: Mapped["Application"] = relationship(
        "Application", back_populates="payments"
    )
    fee_structure: Mapped["FeeStructure"] = relationship(
        "FeeStructure", back_populates="payments"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Payment payment_id={self.payment_id} amount_paid={self.amount_paid}>"
