from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, role_name
from modules.users.models import User
from .models import Notification
from .schema import NotificationCreate, NotificationUpdate

def create_notification(db: Session, notification_data: NotificationCreate, user: User) -> Notification:
    target = db.get(User, notification_data.user_id)
    if target is None: raise HTTPException(status_code=404, detail="Notification user not found.")
    require_same_institution(user, target.institution_id)
    notification = Notification(**notification_data.model_dump()); db.add(notification); db.commit(); db.refresh(notification); return notification

def get_notifications(db: Session, user: User) -> list[Notification]:
    q = db.query(Notification)
    if role_name(user) == "student": q = q.filter(Notification.user_id == user.user_id)
    elif user.institution_id is not None: q = q.join(User, Notification.user_id == User.user_id).filter(User.institution_id == user.institution_id)
    return q.order_by(Notification.sent_at.desc()).all()

def get_notification_by_id(db: Session, notification_id: uuid.UUID, user: User) -> Notification:
    notification = db.get(Notification, notification_id)
    if notification is None: raise HTTPException(status_code=404, detail="Notification not found.")
    if role_name(user) == "student" and notification.user_id != user.user_id: raise HTTPException(status_code=403, detail="You can only access your own notifications.")
    return notification

def update_notification(db: Session, notification_id: uuid.UUID, notification_data: NotificationUpdate, user: User) -> Notification:
    notification = get_notification_by_id(db, notification_id, user)
    for field, value in notification_data.model_dump(exclude_unset=True).items(): setattr(notification, field, value)
    db.commit(); db.refresh(notification); return notification

def delete_notification(db: Session, notification_id: uuid.UUID, user: User) -> None:
    notification = get_notification_by_id(db, notification_id, user)
    db.delete(notification); db.commit()
