import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './routes/ProtectedRoute'
import AuthLayout from './layouts/AuthLayout'
import DashboardLayout from './layouts/DashboardLayout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'
import { RoleRoute, RoleLanding } from './routes/RoleRoute'
import PortalLayout from './features/portals/components/PortalLayout'
import StudentDashboardPage from './features/portals/student/StudentDashboardPage'
import StudentProfilePage from './features/portals/student/StudentProfilePage'
import StudentEducationPage from './features/portals/student/StudentEducationPage'
import StudentEntrancePage from './features/portals/student/StudentEntrancePage'
import StudentApplicationPage from './features/portals/student/StudentApplicationPage'
import StudentDocumentsPage from './features/portals/student/StudentDocumentsPage'
import StudentStatusPage from './features/portals/student/StudentStatusPage'
import OfficerDashboardPage from './features/portals/officer/OfficerDashboardPage'
import OfficerApplicationsPage from './features/portals/officer/OfficerApplicationsPage'
import OfficerApplicationReviewPage from './features/portals/officer/OfficerApplicationReviewPage'
import ReportsListPage from './features/reports/pages/ReportsListPage'

// ---- Institutions ----
import InstitutionsListPage from './features/institutions/pages/InstitutionsListPage'
import InstitutionCreatePage from './features/institutions/pages/InstitutionCreatePage'
import InstitutionEditPage from './features/institutions/pages/InstitutionEditPage'
import InstitutionDetailsPage from './features/institutions/pages/InstitutionDetailsPage'

// ---- Faculties ----
import FacultiesListPage from './features/faculties/pages/FacultiesListPage'
import FacultyCreatePage from './features/faculties/pages/FacultyCreatePage'
import FacultyEditPage from './features/faculties/pages/FacultyEditPage'
import FacultyDetailsPage from './features/faculties/pages/FacultyDetailsPage'

// ---- Departments ----
import DepartmentsListPage from './features/departments/pages/DepartmentsListPage'
import DepartmentCreatePage from './features/departments/pages/DepartmentCreatePage'
import DepartmentEditPage from './features/departments/pages/DepartmentEditPage'
import DepartmentDetailsPage from './features/departments/pages/DepartmentDetailsPage'

// ---- Courses ----
import CoursesListPage from './features/courses/pages/CoursesListPage'
import CourseCreatePage from './features/courses/pages/CourseCreatePage'
import CourseEditPage from './features/courses/pages/CourseEditPage'
import CourseDetailsPage from './features/courses/pages/CourseDetailsPage'

// ---- Admission Cycles ----
import AdmissionCyclesListPage from './features/admission-cycles/pages/AdmissionCyclesListPage'
import AdmissionCycleCreatePage from './features/admission-cycles/pages/AdmissionCycleCreatePage'
import AdmissionCycleEditPage from './features/admission-cycles/pages/AdmissionCycleEditPage'
import AdmissionCycleDetailsPage from './features/admission-cycles/pages/AdmissionCycleDetailsPage'

// ---- Seat Matrix ----
import SeatMatrixListPage from './features/seat-matrix/pages/SeatMatrixListPage'
import SeatMatrixCreatePage from './features/seat-matrix/pages/SeatMatrixCreatePage'
import SeatMatrixEditPage from './features/seat-matrix/pages/SeatMatrixEditPage'
import SeatMatrixDetailsPage from './features/seat-matrix/pages/SeatMatrixDetailsPage'

// ---- Fee Structure ----
import FeeStructureListPage from './features/fee-structure/pages/FeeStructureListPage'
import FeeStructureCreatePage from './features/fee-structure/pages/FeeStructureCreatePage'
import FeeStructureEditPage from './features/fee-structure/pages/FeeStructureEditPage'
import FeeStructureDetailsPage from './features/fee-structure/pages/FeeStructureDetailsPage'

// ---- Users ----
import UsersListPage from './features/users/pages/UsersListPage'
import UserCreatePage from './features/users/pages/UserCreatePage'
import UserEditPage from './features/users/pages/UserEditPage'
import UserDetailsPage from './features/users/pages/UserDetailsPage'

// ---- Roles ----
import RolesListPage from './features/roles/pages/RolesListPage'
import RoleCreatePage from './features/roles/pages/RoleCreatePage'
import RoleEditPage from './features/roles/pages/RoleEditPage'
import RoleDetailsPage from './features/roles/pages/RoleDetailsPage'

// ---- Staff ----
import StaffListPage from './features/staff/pages/StaffListPage'
import StaffCreatePage from './features/staff/pages/StaffCreatePage'
import StaffEditPage from './features/staff/pages/StaffEditPage'
import StaffDetailsPage from './features/staff/pages/StaffDetailsPage'

// ---- Students ----
import StudentsListPage from './features/students/pages/StudentsListPage'
import StudentCreatePage from './features/students/pages/StudentCreatePage'
import StudentEditPage from './features/students/pages/StudentEditPage'
import StudentDetailsPage from './features/students/pages/StudentDetailsPage'

// ---- Educational Details ----
import EducationalDetailsListPage from './features/educational-details/pages/EducationalDetailsListPage'
import EducationalDetailCreatePage from './features/educational-details/pages/EducationalDetailCreatePage'
import EducationalDetailEditPage from './features/educational-details/pages/EducationalDetailEditPage'
import EducationalDetailDetailsPage from './features/educational-details/pages/EducationalDetailDetailsPage'

// ---- Entrance Exam Scores ----
import EntranceExamScoresListPage from './features/entrance-exam-scores/pages/EntranceExamScoresListPage'
import EntranceExamScoreCreatePage from './features/entrance-exam-scores/pages/EntranceExamScoreCreatePage'
import EntranceExamScoreEditPage from './features/entrance-exam-scores/pages/EntranceExamScoreEditPage'
import EntranceExamScoreDetailsPage from './features/entrance-exam-scores/pages/EntranceExamScoreDetailsPage'

// ---- Applications ----
import ApplicationsListPage from './features/applications/pages/ApplicationsListPage'
import ApplicationCreatePage from './features/applications/pages/ApplicationCreatePage'
import ApplicationEditPage from './features/applications/pages/ApplicationEditPage'
import ApplicationDetailsPage from './features/applications/pages/ApplicationDetailsPage'

// ---- Application Preferences ----
import ApplicationPreferencesListPage from './features/application-preferences/pages/ApplicationPreferencesListPage'
import ApplicationPreferenceCreatePage from './features/application-preferences/pages/ApplicationPreferenceCreatePage'
import ApplicationPreferenceEditPage from './features/application-preferences/pages/ApplicationPreferenceEditPage'
import ApplicationPreferenceDetailsPage from './features/application-preferences/pages/ApplicationPreferenceDetailsPage'

// ---- Application Status History ----
import ApplicationStatusHistoryListPage from './features/application-status-history/pages/ApplicationStatusHistoryListPage'
import ApplicationStatusHistoryDetailsPage from './features/application-status-history/pages/ApplicationStatusHistoryDetailsPage'

// ---- Document Types ----
import DocumentTypesListPage from './features/document-types/pages/DocumentTypesListPage'
import DocumentTypeCreatePage from './features/document-types/pages/DocumentTypeCreatePage'
import DocumentTypeEditPage from './features/document-types/pages/DocumentTypeEditPage'
import DocumentTypeDetailsPage from './features/document-types/pages/DocumentTypeDetailsPage'

// ---- Documents ----
import DocumentsListPage from './features/documents/pages/DocumentsListPage'
import DocumentCreatePage from './features/documents/pages/DocumentCreatePage'
import DocumentEditPage from './features/documents/pages/DocumentEditPage'
import DocumentDetailsPage from './features/documents/pages/DocumentDetailsPage'

// ---- AI Verification ----
import AiVerificationListPage from './features/ai-verification/pages/AiVerificationListPage'
import AiVerificationCreatePage from './features/ai-verification/pages/AiVerificationCreatePage'
import AiVerificationEditPage from './features/ai-verification/pages/AiVerificationEditPage'
import AiVerificationDetailsPage from './features/ai-verification/pages/AiVerificationDetailsPage'

// ---- Payments ----
import PaymentsListPage from './features/payments/pages/PaymentsListPage'
import PaymentCreatePage from './features/payments/pages/PaymentCreatePage'
import PaymentEditPage from './features/payments/pages/PaymentEditPage'
import PaymentDetailsPage from './features/payments/pages/PaymentDetailsPage'

// ---- Notifications ----
import NotificationsListPage from './features/notifications/pages/NotificationsListPage'
import NotificationCreatePage from './features/notifications/pages/NotificationCreatePage'
import NotificationEditPage from './features/notifications/pages/NotificationEditPage'
import NotificationDetailsPage from './features/notifications/pages/NotificationDetailsPage'

// ---- Chat History ----
import ChatListPage from './features/chat/pages/ChatListPage'
import ChatCreatePage from './features/chat/pages/ChatCreatePage'
import ChatEditPage from './features/chat/pages/ChatEditPage'
import ChatDetailsPage from './features/chat/pages/ChatDetailsPage'

// ---- Audit Logs ----
import AuditLogsListPage from './features/audit-logs/pages/AuditLogsListPage'
import AuditLogDetailsPage from './features/audit-logs/pages/AuditLogDetailsPage'

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<RoleLanding />} />

        {/* Public routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
           <Route path="/register" element={<Register />} />
        </Route>

        {/* Role-specific admission workflows */}
        <Route element={<ProtectedRoute />}>
          <Route element={<RoleRoute roles={['student']} />}>
            <Route element={<PortalLayout kind="student" />}>
              <Route path="/student" element={<StudentDashboardPage />} />
              <Route path="/student/profile" element={<StudentProfilePage />} />
              <Route path="/student/education" element={<StudentEducationPage />} />
              <Route path="/student/entrance-exam" element={<StudentEntrancePage />} />
              <Route path="/student/application" element={<StudentApplicationPage />} />
              <Route path="/student/documents" element={<StudentDocumentsPage />} />
              <Route path="/student/status" element={<StudentStatusPage />} />
            </Route>
          </Route>
          <Route element={<RoleRoute roles={['admission_officer','department_reviewer']} />}>
            <Route element={<PortalLayout kind="officer" />}>
              <Route path="/officer" element={<OfficerDashboardPage />} />
              <Route path="/officer/applications" element={<OfficerApplicationsPage />} />
              <Route path="/officer/applications/:id" element={<OfficerApplicationReviewPage />} />
            </Route>
          </Route>
        </Route>

        {/* Protected routes — everything here requires a logged-in user */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/settings" element={<Settings />} />

            {/* Institutions */}
            <Route path="/institutions" element={<InstitutionsListPage />} />
            <Route path="/institutions/new" element={<InstitutionCreatePage />} />
            <Route path="/institutions/:id" element={<InstitutionDetailsPage />} />
            <Route path="/institutions/:id/edit" element={<InstitutionEditPage />} />

            {/* Faculties */}
            <Route path="/faculties" element={<FacultiesListPage />} />
            <Route path="/faculties/new" element={<FacultyCreatePage />} />
            <Route path="/faculties/:id" element={<FacultyDetailsPage />} />
            <Route path="/faculties/:id/edit" element={<FacultyEditPage />} />

            {/* Departments */}
            <Route path="/departments" element={<DepartmentsListPage />} />
            <Route path="/departments/new" element={<DepartmentCreatePage />} />
            <Route path="/departments/:id" element={<DepartmentDetailsPage />} />
            <Route path="/departments/:id/edit" element={<DepartmentEditPage />} />

            {/* Courses */}
            <Route path="/courses" element={<CoursesListPage />} />
            <Route path="/courses/new" element={<CourseCreatePage />} />
            <Route path="/courses/:id" element={<CourseDetailsPage />} />
            <Route path="/courses/:id/edit" element={<CourseEditPage />} />

            {/* Admission Cycles */}
            <Route path="/admission-cycles" element={<AdmissionCyclesListPage />} />
            <Route path="/admission-cycles/new" element={<AdmissionCycleCreatePage />} />
            <Route path="/admission-cycles/:id" element={<AdmissionCycleDetailsPage />} />
            <Route path="/admission-cycles/:id/edit" element={<AdmissionCycleEditPage />} />

            {/* Seat Matrix */}
            <Route path="/seat-matrix" element={<SeatMatrixListPage />} />
            <Route path="/seat-matrix/new" element={<SeatMatrixCreatePage />} />
            <Route path="/seat-matrix/:id" element={<SeatMatrixDetailsPage />} />
            <Route path="/seat-matrix/:id/edit" element={<SeatMatrixEditPage />} />

            {/* Fee Structure */}
            <Route path="/fee-structure" element={<FeeStructureListPage />} />
            <Route path="/fee-structure/new" element={<FeeStructureCreatePage />} />
            <Route path="/fee-structure/:id" element={<FeeStructureDetailsPage />} />
            <Route path="/fee-structure/:id/edit" element={<FeeStructureEditPage />} />

            {/* Users */}
            <Route path="/users" element={<UsersListPage />} />
            <Route path="/users/new" element={<UserCreatePage />} />
            <Route path="/users/:id" element={<UserDetailsPage />} />
            <Route path="/users/:id/edit" element={<UserEditPage />} />

            {/* Roles */}
            <Route path="/roles" element={<RolesListPage />} />
            <Route path="/roles/new" element={<RoleCreatePage />} />
            <Route path="/roles/:id" element={<RoleDetailsPage />} />
            <Route path="/roles/:id/edit" element={<RoleEditPage />} />

            {/* Staff */}
            <Route path="/staff" element={<StaffListPage />} />
            <Route path="/staff/new" element={<StaffCreatePage />} />
            <Route path="/staff/:id" element={<StaffDetailsPage />} />
            <Route path="/staff/:id/edit" element={<StaffEditPage />} />

            {/* Students */}
            <Route path="/students" element={<StudentsListPage />} />
            <Route path="/students/new" element={<StudentCreatePage />} />
            <Route path="/students/:id" element={<StudentDetailsPage />} />
            <Route path="/students/:id/edit" element={<StudentEditPage />} />

            {/* Educational Details */}
            <Route path="/educational-details" element={<EducationalDetailsListPage />} />
            <Route path="/educational-details/new" element={<EducationalDetailCreatePage />} />
            <Route path="/educational-details/:id" element={<EducationalDetailDetailsPage />} />
            <Route path="/educational-details/:id/edit" element={<EducationalDetailEditPage />} />

            {/* Entrance Exam Scores */}
            <Route path="/entrance-exam-scores" element={<EntranceExamScoresListPage />} />
            <Route path="/entrance-exam-scores/new" element={<EntranceExamScoreCreatePage />} />
            <Route path="/entrance-exam-scores/:id" element={<EntranceExamScoreDetailsPage />} />
            <Route path="/entrance-exam-scores/:id/edit" element={<EntranceExamScoreEditPage />} />

            {/* Applications */}
            <Route path="/applications" element={<ApplicationsListPage />} />
            <Route path="/applications/new" element={<ApplicationCreatePage />} />
            <Route path="/applications/:id" element={<ApplicationDetailsPage />} />
            <Route path="/applications/:id/edit" element={<ApplicationEditPage />} />

            {/* Application Preferences */}
            <Route path="/application-preferences" element={<ApplicationPreferencesListPage />} />
            <Route path="/application-preferences/new" element={<ApplicationPreferenceCreatePage />} />
            <Route path="/application-preferences/:id" element={<ApplicationPreferenceDetailsPage />} />
            <Route path="/application-preferences/:id/edit" element={<ApplicationPreferenceEditPage />} />

            {/* Application Status History */}
            <Route path="/application-status-history" element={<ApplicationStatusHistoryListPage />} />
            <Route path="/application-status-history/:id" element={<ApplicationStatusHistoryDetailsPage />} />

            {/* Document Types */}
            <Route path="/document-types" element={<DocumentTypesListPage />} />
            <Route path="/document-types/new" element={<DocumentTypeCreatePage />} />
            <Route path="/document-types/:id" element={<DocumentTypeDetailsPage />} />
            <Route path="/document-types/:id/edit" element={<DocumentTypeEditPage />} />

            {/* Documents */}
            <Route path="/documents" element={<DocumentsListPage />} />
            <Route path="/documents/new" element={<DocumentCreatePage />} />
            <Route path="/documents/:id" element={<DocumentDetailsPage />} />
            <Route path="/documents/:id/edit" element={<DocumentEditPage />} />

            {/* AI Verification */}
            <Route path="/ai-verification" element={<AiVerificationListPage />} />
            <Route path="/ai-verification/new" element={<AiVerificationCreatePage />} />
            <Route path="/ai-verification/:id" element={<AiVerificationDetailsPage />} />
            <Route path="/ai-verification/:id/edit" element={<AiVerificationEditPage />} />

            {/* Payments */}
            <Route path="/payments" element={<PaymentsListPage />} />
            <Route path="/payments/new" element={<PaymentCreatePage />} />
            <Route path="/payments/:id" element={<PaymentDetailsPage />} />
            <Route path="/payments/:id/edit" element={<PaymentEditPage />} />

            {/* Notifications */}
            <Route path="/notifications" element={<NotificationsListPage />} />
            <Route path="/notifications/new" element={<NotificationCreatePage />} />
            <Route path="/notifications/:id" element={<NotificationDetailsPage />} />
            <Route path="/notifications/:id/edit" element={<NotificationEditPage />} />

            {/* Chat History */}
            <Route path="/chat" element={<ChatListPage />} />
            <Route path="/chat/new" element={<ChatCreatePage />} />
            <Route path="/chat/:id" element={<ChatDetailsPage />} />
            <Route path="/chat/:id/edit" element={<ChatEditPage />} />

            {/* Reports (read-only) */}
            <Route path="/reports" element={<ReportsListPage />} />

            {/* Audit Logs */}
            <Route path="/audit-logs" element={<AuditLogsListPage />} />
            <Route path="/audit-logs/:id" element={<AuditLogDetailsPage />} />
          </Route>
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  )
}
