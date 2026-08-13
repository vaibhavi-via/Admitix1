"""Validation helpers for institution inputs."""


def validate_institution_name(name: str) -> str:
    value = name.strip()
    if len(value) < 2:
        raise ValueError("Institution name must contain at least 2 characters.")
    return value


def validate_institution_code(code: str) -> str:
    value = code.strip().upper()
    if not value:
        raise ValueError("Institution code is required.")
    return value
