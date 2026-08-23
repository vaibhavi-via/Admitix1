"""
==========================================================
                DATABASE SEED DATA
==========================================================

Populates baseline reference data required for the
application to function — currently the RBAC role
catalogue and an initial Super Admin account.

Run directly:
    python -m db.seed
"""

# ==========================================================
# Import Required Modules
# ==========================================================

from sqlalchemy.orm import Session

from core.security import hash_password
from db.session import SessionLocal
from modules.domains.models import Domain
from modules.roles.models import Role
from modules.users.models import User

# ==========================================================
# Reference Data
# ==========================================================

DOMAIN_DEFS = [
    ("ENG", "Engineering", None),
    ("MED", "Medical", None),
    ("LAW", "Law", None),
    ("PHARM", "Pharmacy", None),
]

ROLE_NAMES = [
    ("super_admin", "Platform-level super administrator"),
    ("institution_admin", "Institution administrator"),
    ("admission_officer", "Handles admission processing"),
    ("department_reviewer", "Reviews department-level applications"),
    ("finance_officer", "Handles fee and payment verification"),
    ("registrar", "Manages academic records"),
    ("faculty", "Teaching staff member"),
    ("student", "Student user"),
    ("guardian", "Guardian/parent of a student"),
]

SUPER_ADMIN_EMAIL = "admin@example.com"
SUPER_ADMIN_PASSWORD = "ChangeMe123!"


# ==========================================================
# Seed Functions
# ==========================================================

def seed_domains(db: Session) -> dict[str, Domain]:
    """Insert any missing domains from DOMAIN_DEFS. Returns code -> Domain map."""

    existing = {domain.domain_code: domain for domain in db.query(Domain).all()}

    for code, name, description in DOMAIN_DEFS:
        if code not in existing:
            domain = Domain(domain_code=code, domain_name=name, description=description)
            db.add(domain)
            existing[code] = domain

    db.flush()
    return existing


def seed_roles(db: Session) -> dict[str, Role]:
    """Insert any missing roles from ROLE_NAMES. Returns name -> Role map."""

    existing = {role.role_name: role for role in db.query(Role).all()}

    for name, description in ROLE_NAMES:
        if name not in existing:
            role = Role(role_name=name, description=description)
            db.add(role)
            existing[name] = role

    db.flush()
    return existing


def seed_super_admin(db: Session, roles: dict[str, Role]) -> None:
    """Create the initial Super Admin user if one doesn't already exist."""

    exists = (
        db.query(User)
        .filter(User.email == SUPER_ADMIN_EMAIL, User.institution_id.is_(None))
        .first()
    )
    if exists:
        return

    super_admin_role = roles["super_admin"]

    admin = User(
        institution_id=None,
        role_id=super_admin_role.role_id,
        first_name="Super",
        last_name="Admin",
        email=SUPER_ADMIN_EMAIL,
        password_hash=hash_password(SUPER_ADMIN_PASSWORD),
        is_active=True,
    )
    db.add(admin)


# ==========================================================
# Entry Point
# ==========================================================

def run_seed() -> None:
    db = SessionLocal()
    try:
        seed_domains(db)
        roles = seed_roles(db)
        seed_super_admin(db, roles)
        db.commit()
        print("Database seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
