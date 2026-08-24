from fastapi import APIRouter, Depends

from core.authentication import get_current_user
from core.permissions import require_module_access

from modules.admission_cycles.router import router as admission_cycles_router
from modules.ai_verification.router import router as ai_verification_router
from modules.ai_document.router import router as ai_document_router
from modules.application_preferences.router import router as application_preferences_router
from modules.applications.router import router as applications_router
from modules.applications.history_router import router as application_status_history_router
from modules.audit_logs.router import router as audit_logs_router
from modules.auth.router import router as auth_router
from modules.chat.router import router as chat_router
from modules.courses.router import router as courses_router
from modules.courses.extra_router import fee_router, seat_router
from modules.dashboard.router import router as dashboard_router
from modules.departments.router import router as departments_router
from modules.document_types.router import router as document_types_router
from modules.domains.router import router as domains_router
from modules.documents.router import router as documents_router
from modules.educational_details.router import router as educational_details_router
from modules.entrance_exam_scores.router import router as entrance_exam_scores_router
from modules.faculties.router import router as faculties_router
from modules.institutions.router import router as institutions_router
from modules.notifications.router import router as notifications_router
from modules.payments.router import router as payments_router
from modules.reports.router import router as reports_router
from modules.roles.router import router as roles_router
from modules.staff.router import router as staff_router
from modules.students.router import router as students_router
from modules.users.router import router as users_router

api_router = APIRouter()

ADMIN = {"super_admin", "institution_admin"}
OFFICER = {"admission_officer"}
STUDENT = {"student"}
ADMIN_OFFICER = ADMIN | OFFICER
ALL_PORTAL = ADMIN | OFFICER | STUDENT


def secure(router, read_roles, write_roles=None):
    return api_router.include_router(
        router,
        dependencies=[
            Depends(get_current_user),
            Depends(require_module_access(read_roles, write_roles)),
        ],
    )


# Authentication endpoints are public except for endpoints that explicitly
# take CurrentUser (logout/change-password/me).
api_router.include_router(auth_router)

# Admin-only configuration and access management.
secure(institutions_router, ADMIN, ADMIN)
secure(domains_router, ADMIN, ADMIN)
secure(roles_router, ADMIN, ADMIN)
secure(staff_router, ADMIN, ADMIN)
secure(users_router, ADMIN, ADMIN)

# Admission officer and admin workspaces.
secure(dashboard_router, ADMIN_OFFICER, ADMIN_OFFICER)
secure(applications_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(application_status_history_router, ADMIN_OFFICER, ADMIN_OFFICER)
secure(students_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(documents_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(payments_router, ALL_PORTAL, ADMIN_OFFICER)
secure(reports_router, ADMIN_OFFICER, ADMIN_OFFICER)
secure(notifications_router, ALL_PORTAL, ADMIN_OFFICER)

# Reference data: officers/students can view, only admins can change.
secure(courses_router, ALL_PORTAL, ADMIN)
secure(departments_router, ALL_PORTAL, ADMIN)
secure(faculties_router, ALL_PORTAL, ADMIN)
secure(admission_cycles_router, ALL_PORTAL, ADMIN)
secure(document_types_router, ALL_PORTAL, ADMIN)
secure(fee_router, ALL_PORTAL, ADMIN)
secure(seat_router, ALL_PORTAL, ADMIN)

# Student-owned admission records can be edited by the student; officers
# review them; admins retain full access.
secure(educational_details_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(entrance_exam_scores_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(application_preferences_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)

# AI/document tooling is an officer/admin capability.
secure(ai_verification_router, ADMIN_OFFICER, ADMIN_OFFICER)
secure(ai_document_router, ADMIN_OFFICER, ADMIN_OFFICER)
secure(chat_router, ALL_PORTAL, ADMIN_OFFICER | STUDENT)
secure(audit_logs_router, ADMIN, ADMIN)
