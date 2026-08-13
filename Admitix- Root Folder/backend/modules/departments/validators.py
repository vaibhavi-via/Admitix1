"""Validation helpers for department inputs."""


def validate_department_code(code: str) -> str:
    value = code.strip().upper()
    if not value:
        raise ValueError("Department code is required.")
    if len(value) > 20:
        raise ValueError("Department code cannot exceed 20 characters.")
    return value
