import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Settings,
  Building2,
  GraduationCap,
  Boxes,
  BookOpen,
  CalendarRange,
  Users,
  ShieldCheck,
  UserCog,
  User,
  FileText,
  ClipboardList,
  FileCheck2,
  FilePlus2,
  Files,
  ScanSearch,
  CreditCard,
  Bell,
  MessageSquare,
  BarChart3,
  History,
  Grid3x3,
  Wallet,
  ListChecks,
  Sparkles,
  ChevronRight,
} from 'lucide-react'
import { APP_NAME } from '../utils/constants'

const NAV_GROUPS = [
  {
    label: 'Overview',
    items: [
      { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    ],
  },
  {
    label: 'Academics',
    items: [
      { to: '/institutions', label: 'Institutions', icon: Building2 },
      { to: '/faculties', label: 'Faculties', icon: GraduationCap },
      { to: '/departments', label: 'Departments', icon: Boxes },
      { to: '/courses', label: 'Courses', icon: BookOpen },
      { to: '/admission-cycles', label: 'Admission Cycles', icon: CalendarRange },
      { to: '/seat-matrix', label: 'Seat Matrix', icon: Grid3x3 },
    ],
  },
  {
    label: 'People & Access',
    items: [
      { to: '/users', label: 'Users', icon: Users },
      { to: '/roles', label: 'Roles', icon: ShieldCheck },
      { to: '/staff', label: 'Staff', icon: UserCog },
      { to: '/students', label: 'Students', icon: User },
    ],
  },
  {
    label: 'Admissions',
    items: [
      {
        to: '/educational-details',
        label: 'Educational Details',
        icon: FileText,
      },
      {
        to: '/entrance-exam-scores',
        label: 'Entrance Exam Scores',
        icon: ClipboardList,
      },
      {
        to: '/applications',
        label: 'Applications',
        icon: FileCheck2,
      },
      {
        to: '/application-preferences',
        label: 'App. Preferences',
        icon: FilePlus2,
      },
      {
        to: '/application-status-history',
        label: 'Status History',
        icon: ListChecks,
      },
    ],
  },
  {
    label: 'Documents',
    items: [
      {
        to: '/document-types',
        label: 'Document Types',
        icon: Files,
      },
      {
        to: '/documents',
        label: 'Documents',
        icon: FileText,
      },
      {
        to: '/ai-verification',
        label: 'AI Verification',
        icon: ScanSearch,
      },
      {
        to: '/ai-document-intelligence',
        label: 'AI Document Intelligence',
        icon: Sparkles,
      },
    ],
  },
  {
    label: 'Operations',
    items: [
      {
        to: '/fee-structure',
        label: 'Fee Structure',
        icon: Wallet,
      },
      {
        to: '/payments',
        label: 'Payments',
        icon: CreditCard,
      },
      {
        to: '/notifications',
        label: 'Notifications',
        icon: Bell,
      },
      {
        to: '/chat',
        label: 'Chat History',
        icon: MessageSquare,
      },
      {
        to: '/reports',
        label: 'Reports',
        icon: BarChart3,
      },
      {
        to: '/audit-logs',
        label: 'Audit Logs',
        icon: History,
      },
    ],
  },
]

export default function Sidebar({ open, onClose }) {
  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-30 bg-black/60 backdrop-blur-sm lg:hidden"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-[270px] flex-col bg-[#0B2117] text-white shadow-2xl transition-transform duration-300 lg:static lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand */}
        <div className="flex h-[72px] shrink-0 items-center border-b border-white/10 px-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500 shadow-lg shadow-emerald-500/20">
              <span className="text-lg font-bold text-white">
                {APP_NAME.charAt(0)}
              </span>
            </div>

            <div>
              <p className="text-[15px] font-semibold tracking-wide text-white">
                {APP_NAME}
              </p>

              <p className="mt-0.5 text-[11px] text-emerald-200/60">
                Administration Portal
              </p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-5">
          <div className="space-y-6">
            {NAV_GROUPS.map((group) => (
              <div key={group.label}>
                <p className="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.14em] text-emerald-200/40">
                  {group.label}
                </p>

                <div className="space-y-1">
                  {group.items.map(({ to, label, icon: Icon }) => (
                    <NavLink
                      key={to}
                      to={to}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium transition-all duration-200 ${
                          isActive
                            ? 'bg-emerald-500/15 text-white'
                            : 'text-slate-400 hover:bg-white/[0.06] hover:text-white'
                        }`
                      }
                    >
                      {({ isActive }) => (
                        <>
                          {/* Green active bar */}
                          {isActive && (
                            <span className="absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-emerald-400" />
                          )}

                          {/* Icon */}
                          <span
                            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition ${
                              isActive
                                ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/20'
                                : 'bg-white/[0.04] text-slate-500 group-hover:bg-emerald-500/10 group-hover:text-emerald-300'
                            }`}
                          >
                            <Icon size={16} strokeWidth={1.8} />
                          </span>

                          {/* Label */}
                          <span className="min-w-0 flex-1 truncate">
                            {label}
                          </span>

                          {/* Arrow */}
                          <ChevronRight
                            size={14}
                            className={`shrink-0 transition-all ${
                              isActive
                                ? 'text-emerald-300 opacity-100'
                                : 'text-slate-600 opacity-0 group-hover:translate-x-0.5 group-hover:opacity-100'
                            }`}
                          />
                        </>
                      )}
                    </NavLink>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </nav>

        {/* Bottom section */}
        <div className="shrink-0 border-t border-white/10 p-3">
          <NavLink
            to="/settings"
            onClick={onClose}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium transition ${
                isActive
                  ? 'bg-emerald-500/15 text-white'
                  : 'text-slate-400 hover:bg-white/[0.06] hover:text-white'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={`flex h-8 w-8 items-center justify-center rounded-lg ${
                    isActive
                      ? 'bg-emerald-500 text-white'
                      : 'bg-white/[0.04] text-slate-500 group-hover:text-emerald-300'
                  }`}
                >
                  <Settings size={16} strokeWidth={1.8} />
                </span>

                <span className="flex-1">Settings</span>

                <ChevronRight
                  size={14}
                  className="text-slate-600 transition group-hover:translate-x-0.5 group-hover:text-emerald-300"
                />
              </>
            )}
          </NavLink>

          <div className="mt-3 rounded-xl border border-emerald-400/10 bg-emerald-400/[0.04] px-3 py-2.5">
            <p className="text-[10px] font-semibold uppercase tracking-wider text-emerald-400/60">
              Admitix
            </p>

            <p className="mt-1 text-[11px] text-slate-500">
              Administration System
            </p>
          </div>
        </div>
      </aside>
    </>
  )
} 