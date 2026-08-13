"""Validation helpers for audit-log payloads."""


def validate_action(action: str) -> str:
    value = action.strip().lower()
    if not value:
        raise ValueError("Audit action is required.")
    return value


def validate_entity_name(entity_name: str) -> str:
    value = entity_name.strip()
    if not value:
        raise ValueError("Entity name is required.")
    return value
