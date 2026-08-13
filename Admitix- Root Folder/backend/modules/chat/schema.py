"""Pydantic (v2) schemas for the `chat_history` resource."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChatHistoryBase(BaseModel):
    question: str = Field(..., min_length=1)


class ChatHistoryCreate(ChatHistoryBase):
    """Payload for `POST /chat` — the student asks a question. The
    `response` is filled in by the AI integration layer, not the
    client."""

    student_id: uuid.UUID


# Fix: add the missing PATCH payload model expected by the router/service
# contract so `ChatHistoryUpdate` can be imported safely.
class ChatHistoryUpdate(BaseModel):
    response: str | None = None


class ChatHistoryRead(ChatHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    chat_id: uuid.UUID
    student_id: uuid.UUID
    response: str | None
    created_at: datetime
