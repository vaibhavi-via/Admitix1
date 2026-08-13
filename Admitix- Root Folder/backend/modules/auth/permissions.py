"""Permission helpers for authentication flows."""
def can_manage_own_session(role_name: str) -> bool:
    return bool(role_name)
def can_manage_accounts(role_name: str) -> bool:
    return role_name in {"super_admin", "institution_admin"}
