"""Business logic for the `notifications` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Notification
from .schema import NotificationCreate, NotificationUpdate


def create_notification(db: Session, notification_data: NotificationCreate) -> Notification:
    """Send/record a new notification for a user."""

    notification = Notification(**notification_data.model_dump())

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_notifications(db: Session) -> list[Notification]:
    """Return every notification, most recently sent first."""

    return db.query(Notification).order_by(Notification.sent_at.desc()).all()


def get_notification_by_id(db: Session, notification_id: uuid.UUID) -> Notification:
    """Fetch a single notification by id or raise 404."""

    notification = (
        db.query(Notification)
        .filter(Notification.notification_id == notification_id)
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found."
        )

    return notification


def update_notification(
    db: Session, notification_id: uuid.UUID, notification_data: NotificationUpdate
) -> Notification:
    """Partially update a notification — in practice, mark as read."""

    notification = get_notification_by_id(db, notification_id)

    update_data = notification_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notification, field, value)

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(db: Session, notification_id: uuid.UUID) -> None:
    """Delete a notification."""

    notification = get_notification_by_id(db, notification_id)

    db.delete(notification)
    db.commit()
