"""Domain-specific exceptions for the `chat_history` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class ChatHistoryNotFoundException(HTTPException):
    """Raised when a chat history entry id does not exist."""

    def __init__(self, detail: str = "Chat history entry not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
