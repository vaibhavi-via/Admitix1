"""Business logic for the `admission_cycles` resource.

Sits between the router (HTTP layer) and the ORM model
(`modules.admission_cycles.models.AdmissionCycle`). Talks directly to the
SQLAlchemy `Session` since `repository.py` is not yet implemented.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import AdmissionCycle
from .schema import AdmissionCycleCreate, AdmissionCycleUpdate


def create_admission_cycle(
    db: Session, admission_cycle_data: AdmissionCycleCreate
) -> AdmissionCycle:
    """Create a new admission cycle for an institution."""

    admission_cycle = AdmissionCycle(**admission_cycle_data.model_dump())

    db.add(admission_cycle)
    db.commit()
    db.refresh(admission_cycle)

    return admission_cycle


def get_admission_cycles(db: Session) -> list[AdmissionCycle]:
    """Return every admission cycle."""

    return db.query(AdmissionCycle).order_by(AdmissionCycle.created_at.desc()).all()


def get_admission_cycle_by_id(
    db: Session, admission_cycle_id: uuid.UUID
) -> AdmissionCycle:
    """Fetch a single admission cycle by id or raise 404."""

    admission_cycle = (
        db.query(AdmissionCycle)
        .filter(AdmissionCycle.cycle_id == admission_cycle_id)
        .first()
    )

    if admission_cycle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission cycle not found.",
        )

    return admission_cycle


def update_admission_cycle(
    db: Session,
    admission_cycle_id: uuid.UUID,
    admission_cycle_data: AdmissionCycleUpdate,
) -> AdmissionCycle:
    """Partially update an admission cycle."""

    admission_cycle = get_admission_cycle_by_id(db, admission_cycle_id)

    update_data = admission_cycle_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(admission_cycle, field, value)

    db.commit()
    db.refresh(admission_cycle)

    return admission_cycle


def delete_admission_cycle(db: Session, admission_cycle_id: uuid.UUID) -> None:
    """Delete an admission cycle."""

    admission_cycle = get_admission_cycle_by_id(db, admission_cycle_id)

    db.delete(admission_cycle)
    db.commit()
