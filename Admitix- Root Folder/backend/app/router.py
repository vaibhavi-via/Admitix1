from fastapi import APIRouter, Depends
from core.authentication import get_current_user

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
api_router.include_router(admission_cycles_router, dependencies=[Depends(get_current_user)])
api_router.include_router(ai_verification_router, dependencies=[Depends(get_current_user)])
api_router.include_router(ai_document_router, dependencies=[Depends(get_current_user)])
api_router.include_router(application_preferences_router, dependencies=[Depends(get_current_user)])
api_router.include_router(applications_router, dependencies=[Depends(get_current_user)])
api_router.include_router(application_status_history_router, dependencies=[Depends(get_current_user)])
api_router.include_router(audit_logs_router, dependencies=[Depends(get_current_user)])
api_router.include_router(auth_router)
api_router.include_router(chat_router, dependencies=[Depends(get_current_user)])
api_router.include_router(courses_router, dependencies=[Depends(get_current_user)])
api_router.include_router(fee_router, dependencies=[Depends(get_current_user)])
api_router.include_router(seat_router, dependencies=[Depends(get_current_user)])
api_router.include_router(dashboard_router, dependencies=[Depends(get_current_user)])
api_router.include_router(departments_router, dependencies=[Depends(get_current_user)])
api_router.include_router(document_types_router, dependencies=[Depends(get_current_user)])
api_router.include_router(documents_router, dependencies=[Depends(get_current_user)])
api_router.include_router(educational_details_router, dependencies=[Depends(get_current_user)])
api_router.include_router(entrance_exam_scores_router, dependencies=[Depends(get_current_user)])
api_router.include_router(faculties_router, dependencies=[Depends(get_current_user)])
api_router.include_router(institutions_router, dependencies=[Depends(get_current_user)])
api_router.include_router(notifications_router, dependencies=[Depends(get_current_user)])
api_router.include_router(payments_router, dependencies=[Depends(get_current_user)])
api_router.include_router(reports_router, dependencies=[Depends(get_current_user)])
api_router.include_router(roles_router, dependencies=[Depends(get_current_user)])
api_router.include_router(staff_router, dependencies=[Depends(get_current_user)])
api_router.include_router(students_router, dependencies=[Depends(get_current_user)])
api_router.include_router(users_router, dependencies=[Depends(get_current_user)])
