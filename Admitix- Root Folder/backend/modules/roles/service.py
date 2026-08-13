"""Business logic for the `roles` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Role
from .schema import RoleCreate, RoleUpdate


def _ensure_unique_role_name(
    db: Session, role_name: str, exclude_role_id: uuid.UUID | None = None
) -> None:
    query = db.query(Role).filter(Role.role_name == role_name)
    if exclude_role_id is not None:
        query = query.filter(Role.role_id != exclude_role_id)

    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role '{role_name}' already exists.",
        )


def create_role(db: Session, role_data: RoleCreate) -> Role:
    """Create a new RBAC role."""

    _ensure_unique_role_name(db, role_data.role_name)

    role = Role(**role_data.model_dump())

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


def get_roles(db: Session) -> list[Role]:
    """Return every role."""

    return db.query(Role).order_by(Role.role_name).all()


def get_role_by_id(db: Session, role_id: uuid.UUID) -> Role:
    """Fetch a single role by id or raise 404."""

    role = db.query(Role).filter(Role.role_id == role_id).first()

    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")

    return role


def update_role(db: Session, role_id: uuid.UUID, role_data: RoleUpdate) -> Role:
    """Partially update a role."""

    role = get_role_by_id(db, role_id)

    update_data = role_data.model_dump(exclude_unset=True)

    if "role_name" in update_data and update_data["role_name"]:
        _ensure_unique_role_name(db, update_data["role_name"], exclude_role_id=role_id)

    for field, value in update_data.items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)

    return role


def delete_role(db: Session, role_id: uuid.UUID) -> None:
    """Delete a role."""

    role = get_role_by_id(db, role_id)

    db.delete(role)
    db.commit()
