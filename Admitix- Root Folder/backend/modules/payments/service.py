"""Business logic for the `payments` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Payment
from .schema import PaymentCreate, PaymentUpdate


def _ensure_unique_transaction_id(db: Session, transaction_id: str | None) -> None:
    if not transaction_id:
        return

    exists = (
        db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
    )
    if exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Transaction id '{transaction_id}' has already been recorded.",
        )


def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
    """Record a new fee payment against an application. Starts in
    `pending` status by default (model server default) until a
    payment gateway callback / manual update confirms it."""

    _ensure_unique_transaction_id(db, payment_data.transaction_id)

    payment = Payment(**payment_data.model_dump())

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


def get_payments(db: Session) -> list[Payment]:
    """Return every payment, most recent first."""

    return db.query(Payment).order_by(Payment.payment_date.desc()).all()


def get_payment_by_id(db: Session, payment_id: uuid.UUID) -> Payment:
    """Fetch a single payment by id or raise 404."""

    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found."
        )

    return payment


def update_payment(db: Session, payment_id: uuid.UUID, payment_data: PaymentUpdate) -> Payment:
    """Partially update a payment — typically confirming/failing it
    and attaching the gateway `transaction_id`."""

    payment = get_payment_by_id(db, payment_id)

    update_data = payment_data.model_dump(exclude_unset=True)

    if "transaction_id" in update_data and update_data["transaction_id"]:
        if update_data["transaction_id"] != payment.transaction_id:
            _ensure_unique_transaction_id(db, update_data["transaction_id"])

    for field, value in update_data.items():
        setattr(payment, field, value)

    db.commit()
    db.refresh(payment)

    return payment


def delete_payment(db: Session, payment_id: uuid.UUID) -> None:
    """Delete a payment."""

    payment = get_payment_by_id(db, payment_id)

    db.delete(payment)
    db.commit()
