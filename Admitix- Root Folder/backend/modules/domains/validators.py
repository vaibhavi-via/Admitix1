"""Validation helpers for domain inputs."""


def validate_domain_code(code: str) -> str:
    value = code.strip().upper()
    if not value:
        raise ValueError("Domain code is required.")
    return value


def validate_domain_name(name: str) -> str:
    value = name.strip()
    if len(value) < 2:
        raise ValueError("Domain name must contain at least 2 characters.")
    return value
