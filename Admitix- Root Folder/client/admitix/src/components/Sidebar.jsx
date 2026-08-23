import { useEffect, useMemo, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
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
  const location = useLocation()

  // Which group contains the currently active route — used both to
  // auto-expand that group on navigation and as the default open
  // group on first render, so users always land somewhere useful.
  const activeGroupLabel = useMemo(() => {
    const match = NAV_GROUPS.find((group) =>
      group.items.some((item) => location.pathname.startsWith(item.to)),
    )
    return match?.label ?? NAV_GROUPS[0].label
  }, [location.pathname])

  // Collapsible groups keep the sidebar short: only one section's
  // links are visible at a time by default, instead of every single
  // link across every module being rendered at once.
  const [expandedLabel, setExpandedLabel] = useState(activeGroupLabel)

  useEffect(() => {
    setExpandedLabel(activeGroupLabel)
  }, [activeGroupLabel])

  const toggleGroup = (label) => {
    setExpandedLabel((current) => (current === label ? null : label))
  }

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
        <nav className="flex-1 overflow-y-auto px-3 py-4">
          <div className="space-y-1">
            {NAV_GROUPS.map((group) => {
              const isExpanded = expandedLabel === group.label
              const isGroupActive = group.items.some((item) =>
                location.pathname.startsWith(item.to),
              )

              return (
                <div key={group.label}>
                  {/* Group header — click to expand/collapse (dropdown) */}
                  <button
                    type="button"
                    onClick={() => toggleGroup(group.label)}
                    aria-expanded={isExpanded}
                    className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-[10px] font-semibold uppercase tracking-[0.14em] transition ${
                      isGroupActive
                        ? 'text-emerald-300'
                        : 'text-emerald-200/40 hover:text-emerald-200/70'
                    }`}
                  >
                    {group.label}

                    <ChevronRight
                      size={13}
                      className={`shrink-0 transition-transform duration-200 ${
                        isExpanded ? 'rotate-90' : ''
                      }`}
                    />
                  </button>

                  {/* Group links */}
                  <div
                    className={`grid transition-all duration-200 ease-out ${
                      isExpanded
                        ? 'grid-rows-[1fr] opacity-100'
                        : 'grid-rows-[0fr] opacity-0'
                    }`}
                  >
                    <div className="overflow-hidden">
                      <div className="space-y-1 pb-2 pt-1">
                        {group.items.map(({ to, label, icon: Icon }) => (
                          <NavLink
                            key={to}
                            to={to}
                            onClick={onClose}
                            className={({ isActive }) =>
                              `group relative flex items-center gap-3 rounded-xl px-3 py-2 text-[13px] font-medium transition-all duration-200 ${
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
                                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition ${
                                    isActive
                                      ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/20'
                                      : 'bg-white/[0.04] text-slate-500 group-hover:bg-emerald-500/10 group-hover:text-emerald-300'
                                  }`}
                                >
                                  <Icon size={15} strokeWidth={1.8} />
                                </span>

                                {/* Label */}
                                <span className="min-w-0 flex-1 truncate">
                                  {label}
                                </span>
                              </>
                            )}
                          </NavLink>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
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
        </div>
      </aside>
    </>
  )
}