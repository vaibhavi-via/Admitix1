"""Pydantic (v2) schemas for the `notifications` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core.enums import NotificationType


class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    message: str
    notification_type: NotificationType = NotificationType.IN_APP


class NotificationCreate(NotificationBase):
    user_id: uuid.UUID


class NotificationUpdate(BaseModel):
    """Payload for `PATCH /notifications/{notification_id}` — in
    practice used only to mark a notification as read."""

    is_read: bool | None = None


class NotificationRead(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    notification_id: uuid.UUID
    user_id: uuid.UUID
    is_read: bool
    sent_at: datetime
