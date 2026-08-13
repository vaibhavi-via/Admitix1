"""Role checks for document-type configuration."""
READ_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer", "student"})
WRITE_ROLES = frozenset({"super_admin", "institution_admin", "admission_officer"})
def can_read(role_name: str) -> bool: return role_name in READ_ROLES
def can_write(role_name: str) -> bool: return role_name in WRITE_ROLES
