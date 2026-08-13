"""Role checks for application operations."""
READ_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "department_reviewer", "registrar", "student"})
WRITE_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "student"})
def can_read(role_name: str) -> bool: return role_name in READ_ROLES
def can_write(role_name: str) -> bool: return role_name in WRITE_ROLES
