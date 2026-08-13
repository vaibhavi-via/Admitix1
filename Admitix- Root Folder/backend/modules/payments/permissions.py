"""Role checks for payment records."""

READ_ROLES = frozenset({"super_admin", "institution_admin", "finance_officer", "registrar", "student"})
WRITE_ROLES = frozenset({"super_admin", "institution_admin", "finance_officer"})


def can_read(role_name: str) -> bool:
    return role_name in READ_ROLES


def can_write(role_name: str) -> bool:
    return role_name in WRITE_ROLES
