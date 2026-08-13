"""Business logic for the `chat_history` resource.

Note: `router.py` imports `ChatHistoryUpdate` from `.schema`, but
`schema.py` currently only defines `ChatHistoryBase`, `ChatHistoryCreate`
and `ChatHistoryRead` — `ChatHistoryUpdate` is missing. To keep this
module importable as-is, `update_chat_history` below accepts the
update payload as `Any` (duck-typed on `.model_dump(exclude_unset=True)`)
rather than importing the missing class. Add a
`ChatHistoryUpdate(BaseModel)` (e.g. `response: str | None = None`) to
`schema.py` to close this gap.
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import ChatHistory
from .schema import ChatHistoryCreate


def create_chat_history(db: Session, chat_history_data: ChatHistoryCreate) -> ChatHistory:
    """Record a student's chat question. `response` is left `None`
    here for the AI integration layer to fill in afterward."""

    chat_history = ChatHistory(**chat_history_data.model_dump())

    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)

    return chat_history


def get_chat_histories(db: Session) -> list[ChatHistory]:
    """Return every chat history entry, most recent first."""

    return db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).all()


def get_chat_history_by_id(db: Session, chat_history_id: uuid.UUID) -> ChatHistory:
    """Fetch a single chat history entry by id or raise 404."""

    chat_history = (
        db.query(ChatHistory).filter(ChatHistory.chat_id == chat_history_id).first()
    )

    if chat_history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat history entry not found.",
        )

    return chat_history


def update_chat_history(
    db: Session, chat_history_id: uuid.UUID, chat_history_data: Any
) -> ChatHistory:
    """Partially update a chat history entry (typically to fill in the
    AI-generated `response`)."""

    chat_history = get_chat_history_by_id(db, chat_history_id)

    update_data = chat_history_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(chat_history, field, value)

    db.commit()
    db.refresh(chat_history)

    return chat_history


def delete_chat_history(db: Session, chat_history_id: uuid.UUID) -> None:
    """Delete a chat history entry."""

    chat_history = get_chat_history_by_id(db, chat_history_id)

    db.delete(chat_history)
    db.commit()
