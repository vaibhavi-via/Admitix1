"""Business logic for the `domains` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Domain
from .schema import DomainCreate, DomainUpdate


def _ensure_unique_domain_code(
    db: Session, domain_code: str, exclude_domain_id: uuid.UUID | None = None
) -> None:
    query = db.query(Domain).filter(Domain.domain_code == domain_code)
    if exclude_domain_id is not None:
        query = query.filter(Domain.domain_id != exclude_domain_id)

    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Domain code '{domain_code}' is already in use.",
        )


def create_domain(db: Session, domain_data: DomainCreate) -> Domain:
    """Create a new domain (academic/professional field)."""

    _ensure_unique_domain_code(db, domain_data.domain_code)

    domain = Domain(**domain_data.model_dump())

    db.add(domain)
    db.commit()
    db.refresh(domain)

    return domain


def get_domains(db: Session) -> list[Domain]:
    """Return every domain."""

    return db.query(Domain).order_by(Domain.domain_name).all()


def get_domain_by_id(db: Session, domain_id: uuid.UUID) -> Domain:
    """Fetch a single domain by id or raise 404."""

    domain = db.query(Domain).filter(Domain.domain_id == domain_id).first()

    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found."
        )

    return domain


def update_domain(
    db: Session, domain_id: uuid.UUID, domain_data: DomainUpdate
) -> Domain:
    """Partially update a domain."""

    domain = get_domain_by_id(db, domain_id)

    update_data = domain_data.model_dump(exclude_unset=True)

    if "domain_code" in update_data and update_data["domain_code"]:
        _ensure_unique_domain_code(
            db, update_data["domain_code"], exclude_domain_id=domain_id
        )

    for field, value in update_data.items():
        setattr(domain, field, value)

    db.commit()
    db.refresh(domain)

    return domain


def delete_domain(db: Session, domain_id: uuid.UUID) -> None:
    """Delete a domain."""

    domain = get_domain_by_id(db, domain_id)

    db.delete(domain)
    db.commit()
