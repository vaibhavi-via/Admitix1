import { useAuth } from '../context/AuthContext'
import {
  Users,
  ClipboardList,
  TrendingUp,
  Clock,
  Building2,
  GraduationCap,
  BookOpen,
  FileCheck2,
  ArrowUpRight,
  ArrowRight,
  CheckCircle2,
  CalendarDays,
  UserPlus,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const STATS = [
  {
    label: 'Total Records',
    value: '128',
    change: '+8.2%',
    description: 'from last month',
    icon: ClipboardList,
    iconBg: 'bg-emerald-50',
    iconColor: 'text-emerald-600',
  },
  {
    label: 'Active Users',
    value: '24',
    change: '+4.5%',
    description: 'from last month',
    icon: Users,
    iconBg: 'bg-blue-50',
    iconColor: 'text-blue-600',
  },
  {
    label: 'Growth',
    value: '+12%',
    change: '+2.4%',
    description: 'from last month',
    icon: TrendingUp,
    iconBg: 'bg-violet-50',
    iconColor: 'text-violet-600',
  },
  {
    label: 'Pending',
    value: '5',
    change: '-2',
    description: 'from last month',
    icon: Clock,
    iconBg: 'bg-amber-50',
    iconColor: 'text-amber-600',
  },
]

const QUICK_ACTIONS = [
  {
    label: 'Add Institution',
    description: 'Register a new institution',
    icon: Building2,
    path: '/institutions/new',
  },
  {
    label: 'Add Faculty',
    description: 'Create a faculty record',
    icon: GraduationCap,
    path: '/faculties/new',
  },
  {
    label: 'Add Course',
    description: 'Create a new course',
    icon: BookOpen,
    path: '/courses/new',
  },
  {
    label: 'View Applications',
    description: 'Review applications',
    icon: FileCheck2,
    path: '/applications',
  },
]

const RECENT_ACTIVITY = [
  {
    title: 'New institution added',
    description: 'Institution registration completed',
    time: '10 minutes ago',
    icon: Building2,
  },
  {
    title: 'Faculty record updated',
    description: 'Faculty information was updated',
    time: '32 minutes ago',
    icon: GraduationCap,
  },
  {
    title: 'Application received',
    description: 'A new admission application was submitted',
    time: '1 hour ago',
    icon: FileCheck2,
  },
  {
    title: 'New user registered',
    description: 'A new user joined the platform',
    time: '2 hours ago',
    icon: UserPlus,
  },
]

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const firstName = user?.name?.split(' ')[0] || 'there'

  return (
    <div className="mx-auto max-w-[1600px] space-y-6">
      {/* =====================================================
          WELCOME SECTION
      ====================================================== */}
      <section className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-700 via-emerald-600 to-green-500 px-6 py-7 text-white shadow-lg shadow-emerald-900/10 sm:px-8">
        {/* Decorative shapes */}
        <div className="pointer-events-none absolute -right-12 -top-20 h-56 w-56 rounded-full bg-white/10" />
        <div className="pointer-events-none absolute -bottom-28 right-32 h-48 w-48 rounded-full bg-white/[0.06]" />

        <div className="relative max-w-2xl">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-xs font-medium text-emerald-50 backdrop-blur">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-200" />
            Administration Portal
          </div>

          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Welcome back, {firstName}! 👋
          </h1>

          <p className="mt-2 max-w-xl text-sm leading-6 text-emerald-50/80 sm:text-[15px]">
            Manage your institutions, faculty, students, applications and
            admission operations from one place.
          </p>

          <div className="mt-5 flex flex-wrap gap-3">
            <button
              onClick={() => navigate('/applications')}
              className="inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-emerald-700 shadow-sm hover:bg-emerald-50"
            >
              View Applications
              <ArrowUpRight size={16} />
            </button>

            <button
              onClick={() => navigate('/institutions')}
              className="inline-flex items-center gap-2 rounded-lg border border-white/20 bg-white/10 px-4 py-2.5 text-sm font-medium text-white backdrop-blur hover:bg-white/20"
            >
              Manage Institutions
            </button>
          </div>
        </div>
      </section>

      {/* =====================================================
          STATISTICS
      ====================================================== */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-slate-900">
              Overview
            </h2>
            <p className="mt-0.5 text-xs text-slate-500">
              Key platform statistics
            </p>
          </div>

          <span className="hidden text-xs text-slate-400 sm:block">
            Updated just now
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {STATS.map(
            ({
              label,
              value,
              change,
              description,
              icon: Icon,
              iconBg,
              iconColor,
            }) => (
              <div
                key={label}
                className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
              >
                <div className="flex items-start justify-between">
                  <div
                    className={`flex h-11 w-11 items-center justify-center rounded-xl ${iconBg} ${iconColor}`}
                  >
                    <Icon size={20} strokeWidth={1.8} />
                  </div>

                  <ArrowUpRight
                    size={17}
                    className="text-slate-300 transition group-hover:text-emerald-500"
                  />
                </div>

                <div className="mt-5">
                  <p className="text-2xl font-bold tracking-tight text-slate-900">
                    {value}
                  </p>

                  <p className="mt-1 text-sm font-medium text-slate-600">
                    {label}
                  </p>

                  <div className="mt-2 flex items-center gap-1.5 text-xs">
                    <span className="font-semibold text-emerald-600">
                      {change}
                    </span>

                    <span className="text-slate-400">
                      {description}
                    </span>
                  </div>
                </div>
              </div>
            ),
          )}
        </div>
      </section>

      {/* =====================================================
          MAIN CONTENT
      ====================================================== */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {/* Recent activity */}
        <section className="xl:col-span-2">
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 sm:px-6">
              <div>
                <h2 className="text-sm font-semibold text-slate-900">
                  Recent Activity
                </h2>

                <p className="mt-0.5 text-xs text-slate-400">
                  Latest activity across your system
                </p>
              </div>

              <button
                onClick={() => navigate('/audit-logs')}
                className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 hover:text-emerald-700"
              >
                View all
                <ArrowRight size={14} />
              </button>
            </div>

            <div className="divide-y divide-slate-100">
              {RECENT_ACTIVITY.map(
                ({ title, description, time, icon: Icon }) => (
                  <div
                    key={title}
                    className="flex items-center gap-4 px-5 py-4 transition hover:bg-slate-50 sm:px-6"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                      <Icon size={18} strokeWidth={1.8} />
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-slate-800">
                        {title}
                      </p>

                      <p className="mt-0.5 truncate text-xs text-slate-400">
                        {description}
                      </p>
                    </div>

                    <span className="hidden shrink-0 text-xs text-slate-400 sm:block">
                      {time}
                    </span>
                  </div>
                ),
              )}
            </div>
          </div>
        </section>

        {/* Quick actions */}
        <section>
          <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-100 px-5 py-4">
              <h2 className="text-sm font-semibold text-slate-900">
                Quick Actions
              </h2>

              <p className="mt-0.5 text-xs text-slate-400">
                Frequently used actions
              </p>
            </div>

            <div className="space-y-1.5 p-3">
              {QUICK_ACTIONS.map(
                ({ label, description, icon: Icon, path }) => (
                  <button
                    key={label}
                    onClick={() => navigate(path)}
                    className="group flex w-full items-center gap-3 rounded-xl p-3 text-left hover:bg-emerald-50"
                  >
                    <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500 transition group-hover:bg-emerald-100 group-hover:text-emerald-600">
                      <Icon size={18} strokeWidth={1.8} />
                    </span>

                    <span className="min-w-0 flex-1">
                      <span className="block text-sm font-medium text-slate-700 group-hover:text-emerald-700">
                        {label}
                      </span>

                      <span className="mt-0.5 block truncate text-xs text-slate-400">
                        {description}
                      </span>
                    </span>

                    <ArrowRight
                      size={15}
                      className="text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-emerald-500"
                    />
                  </button>
                ),
              )}
            </div>
          </div>
        </section>
      </div>

      {/* =====================================================
          SYSTEM STATUS
      ====================================================== */}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
              <CheckCircle2 size={20} />
            </div>

            <div>
              <h2 className="text-sm font-semibold text-slate-900">
                System Status
              </h2>

              <p className="mt-0.5 text-xs text-slate-400">
                All core services are operational
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-slate-500">API</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-slate-500">Database</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-slate-500">Authentication</span>
            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          FOOTER NOTE
      ====================================================== */}
      <div className="flex items-center justify-center gap-2 pb-2 text-xs text-slate-400">
        <CalendarDays size={14} />
        <span>Admitix Administration System</span>
      </div>
    </div>
  )
}