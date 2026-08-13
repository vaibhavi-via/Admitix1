"""Validation helpers for chat messages."""


def validate_message_content(content: str, *, max_length: int = 10_000) -> str:
    value = content.strip()
    if not value:
        raise ValueError("Message content cannot be empty.")
    if len(value) > max_length:
        raise ValueError(f"Message content cannot exceed {max_length} characters.")
    return value
