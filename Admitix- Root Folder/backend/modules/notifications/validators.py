"""Validation helpers for notifications."""


def validate_notification_message(message: str, *, max_length: int = 2_000) -> str:
    value = message.strip()
    if not value:
        raise ValueError("Notification message cannot be empty.")
    if len(value) > max_length:
        raise ValueError(f"Notification message cannot exceed {max_length} characters.")
    return value
