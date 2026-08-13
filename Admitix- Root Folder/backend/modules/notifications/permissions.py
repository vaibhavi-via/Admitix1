"""Role checks for notifications."""

READ_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "finance_officer", "registrar", "faculty", "student", "guardian"})
WRITE_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "finance_officer", "registrar"})


def can_read(role_name: str) -> bool:
    return role_name in READ_ROLES


def can_write(role_name: str) -> bool:
    return role_name in WRITE_ROLES
