"""Validation helpers for user and staff inputs."""

import re

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> str:
    value = email.strip().lower()
    if not EMAIL_PATTERN.fullmatch(value):
        raise ValueError("A valid email address is required.")
    return value


def validate_name(name: str, field_name: str) -> str:
    value = name.strip()
    if not value:
        raise ValueError(f"{field_name} is required.")
    if len(value) > 100:
        raise ValueError(f"{field_name} cannot exceed 100 characters.")
    return value
