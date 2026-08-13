"""Validation helpers for authentication inputs."""

import re

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> str:
    value = email.strip().lower()
    if not EMAIL_PATTERN.fullmatch(value):
        raise ValueError("A valid email address is required.")
    return value


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
