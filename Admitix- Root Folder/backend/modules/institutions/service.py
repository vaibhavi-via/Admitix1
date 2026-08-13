"""Business logic for the `institutions` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Institution
from .schema import InstitutionCreate, InstitutionUpdate


def _ensure_unique_institution_code(
    db: Session, institution_code: str, exclude_institution_id: uuid.UUID | None = None
) -> None:
    query = db.query(Institution).filter(
        Institution.institution_code == institution_code
    )
    if exclude_institution_id is not None:
        query = query.filter(Institution.institution_id != exclude_institution_id)

    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Institution code '{institution_code}' is already in use.",
        )


def create_institution(db: Session, institution_data: InstitutionCreate) -> Institution:
    """Create a new institution (tenant)."""

    _ensure_unique_institution_code(db, institution_data.institution_code)

    institution = Institution(**institution_data.model_dump())

    db.add(institution)
    db.commit()
    db.refresh(institution)

    return institution


def get_institutions(db: Session) -> list[Institution]:
    """Return every institution."""

    return db.query(Institution).order_by(Institution.institution_name).all()


def get_institution_by_id(db: Session, institution_id: uuid.UUID) -> Institution:
    """Fetch a single institution by id or raise 404."""

    institution = (
        db.query(Institution)
        .filter(Institution.institution_id == institution_id)
        .first()
    )

    if institution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found."
        )

    return institution


def update_institution(
    db: Session, institution_id: uuid.UUID, institution_data: InstitutionUpdate
) -> Institution:
    """Partially update an institution."""

    institution = get_institution_by_id(db, institution_id)

    update_data = institution_data.model_dump(exclude_unset=True)

    if "institution_code" in update_data and update_data["institution_code"]:
        _ensure_unique_institution_code(
            db, update_data["institution_code"], exclude_institution_id=institution_id
        )

    for field, value in update_data.items():
        setattr(institution, field, value)

    db.commit()
    db.refresh(institution)

    return institution


def delete_institution(db: Session, institution_id: uuid.UUID) -> None:
    """Delete an institution."""

    institution = get_institution_by_id(db, institution_id)

    db.delete(institution)
    db.commit()
