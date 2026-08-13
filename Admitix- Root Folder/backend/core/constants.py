"""Stable application constants shared by routes, services, and policies."""

from __future__ import annotations


API_V1_PREFIX = "/api/v1"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

ROLE_SUPER_ADMIN = "super_admin"
ROLE_INSTITUTION_ADMIN = "institution_admin"
ROLE_ADMISSION_OFFICER = "admission_officer"
ROLE_DEPARTMENT_REVIEWER = "department_reviewer"
ROLE_FINANCE_OFFICER = "finance_officer"
ROLE_REGISTRAR = "registrar"
ROLE_FACULTY = "faculty"
ROLE_STUDENT = "student"
ROLE_GUARDIAN = "guardian"

ADMIN_ROLES = frozenset({ROLE_SUPER_ADMIN, ROLE_INSTITUTION_ADMIN})
STAFF_ROLES = frozenset(
    {
        ROLE_SUPER_ADMIN,
        ROLE_INSTITUTION_ADMIN,
        ROLE_ADMISSION_OFFICER,
        ROLE_DEPARTMENT_REVIEWER,
        ROLE_FINANCE_OFFICER,
        ROLE_REGISTRAR,
        ROLE_FACULTY,
    }
)
