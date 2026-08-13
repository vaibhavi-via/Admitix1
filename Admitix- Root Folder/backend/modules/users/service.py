"""Business logic for the `users` resource.

`Staff` (also defined in this module's `models.py`/`schema.py`) has no
dedicated routes of its own — the router only exposes CRUD for `User`
itself. This module therefore only implements the `User` operations
the router calls.

Password hashing is delegated to `modules.auth.service.hash_password`
so there is a single implementation of the hashing scheme shared by
both login and account-creation/reset flows.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from modules.auth.service import hash_password

from .models import User
from .schema import UserCreate, UserUpdate


def _ensure_unique_email(
    db: Session,
    email: str,
    institution_id: uuid.UUID | None,
    exclude_user_id: uuid.UUID | None = None,
) -> None:
    """Mirrors the two partial unique indexes on `users.email`: unique
    within an institution, and unique among Super Admins (no
    institution)."""

    query = db.query(User).filter(User.email == email)
    query = query.filter(User.institution_id == institution_id)
    if exclude_user_id is not None:
        query = query.filter(User.user_id != exclude_user_id)

    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email}' is already in use for this institution.",
        )


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user account. Hashes the plaintext `password`
    before persistence — `password_hash` is never accepted directly
    from a client."""

    _ensure_unique_email(db, user_data.email, user_data.institution_id)

    payload = user_data.model_dump(exclude={"password"})
    user = User(**payload, password_hash=hash_password(user_data.password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session) -> list[User]:
    """Return every user."""

    return db.query(User).order_by(User.created_at.desc()).all()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User:
    """Fetch a single user by id or raise 404."""

    user = db.query(User).filter(User.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


def update_user(db: Session, user_id: uuid.UUID, user_data: UserUpdate) -> User:
    """Partially update a user. Password changes go through
    `modules.auth.service.change_password`, not this endpoint."""

    user = get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"]:
        _ensure_unique_email(
            db, update_data["email"], user.institution_id, exclude_user_id=user_id
        )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: uuid.UUID) -> None:
    """Delete a user (cascades to their staff/student profile per the
    model's relationship config)."""

    user = get_user_by_id(db, user_id)

    db.delete(user)
    db.commit()
