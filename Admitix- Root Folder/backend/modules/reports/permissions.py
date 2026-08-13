"""Role checks for institution reports."""

READ_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "finance_officer", "registrar"})


def can_read(role_name: str) -> bool:
    return role_name in READ_ROLES
