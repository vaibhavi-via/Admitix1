"""Business logic for the `ai_verifications` resource."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import AIVerification
from .schema import AIVerificationCreate, AIVerificationUpdate


def create_ai_verification(
    db: Session, ai_verification_data: AIVerificationCreate
) -> AIVerification:
    """Record an AI/OCR verification result for a document."""

    ai_verification = AIVerification(**ai_verification_data.model_dump())

    db.add(ai_verification)
    db.commit()
    db.refresh(ai_verification)

    return ai_verification


def get_ai_verifications(db: Session) -> list[AIVerification]:
    """Return every AI verification record."""

    return db.query(AIVerification).all()


def get_ai_verification_by_id(
    db: Session, verification_id: uuid.UUID
) -> AIVerification:
    """Fetch a single AI verification record by id or raise 404."""

    ai_verification = (
        db.query(AIVerification)
        .filter(AIVerification.verification_id == verification_id)
        .first()
    )

    if ai_verification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI verification record not found.",
        )

    return ai_verification


def update_ai_verification(
    db: Session,
    verification_id: uuid.UUID,
    ai_verification_data: AIVerificationUpdate,
) -> AIVerification:
    """Partially update an AI verification record.

    Automatically stamps `verified_at` the first time the `status`
    moves away from `pending`, unless the caller explicitly supplied
    a `verified_at` value.
    """

    ai_verification = get_ai_verification_by_id(db, verification_id)

    update_data = ai_verification_data.model_dump(exclude_unset=True)

    if update_data.get("status") and "verified_at" not in update_data:
        update_data["verified_at"] = datetime.now(timezone.utc)

    for field, value in update_data.items():
        setattr(ai_verification, field, value)

    db.commit()
    db.refresh(ai_verification)

    return ai_verification


def delete_ai_verification(db: Session, verification_id: uuid.UUID) -> None:
    """Delete an AI verification record."""

    ai_verification = get_ai_verification_by_id(db, verification_id)

    db.delete(ai_verification)
    db.commit()
