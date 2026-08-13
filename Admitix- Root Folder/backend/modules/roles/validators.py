"""Validation helpers for role management."""


def validate_role_name(role_name: str) -> str:
    value = role_name.strip().lower().replace(" ", "_")
    if not value:
        raise ValueError("Role name is required.")
    if len(value) > 50:
        raise ValueError("Role name cannot exceed 50 characters.")
    return value
