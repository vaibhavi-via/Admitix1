
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../../../context/AuthContext'
import { LayoutDashboard, UserRound, GraduationCap, ClipboardList, FileText, Upload, CheckCircle2, LogOut, UsersRound, Search, ShieldCheck } from 'lucide-react'

const studentNav = [
  ['/student','Dashboard',LayoutDashboard],
  ['/student/profile','My Profile',UserRound],
  ['/student/education','Educational Details',GraduationCap],
  ['/student/entrance-exam','Entrance Exam',ClipboardList],
  ['/student/application','My Application',FileText],
  ['/student/documents','Documents',Upload],
  ['/student/status','Application Status',CheckCircle2],
]
const officerNav = [
  ['/officer','Dashboard',LayoutDashboard],
  ['/officer/applications','Applications',Search],
]

export default function PortalLayout({ kind='student' }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const items = kind === 'student' ? studentNav : officerNav
  const title = kind === 'student' ? 'Student Portal' : 'Admission Officer'
  const subtitle = kind === 'student' ? 'Admission workspace' : 'Application processing'

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="flex min-h-screen">
        <aside className="hidden w-[260px] shrink-0 flex-col bg-[#0B2117] text-white lg:flex">
          <div className="flex h-[72px] items-center gap-3 border-b border-white/10 px-5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500 font-bold">A</div>
            <div>
              <div className="text-[15px] font-semibold">Admitix</div>
              <div className="text-[11px] text-emerald-200/60">{subtitle}</div>
            </div>
          </div>
          <nav className="flex-1 space-y-1 p-3">
            {items.map(([to,label,Icon]) => (
              <NavLink key={to} to={to} end={to === `/student` || to === `/officer`}
                className={({isActive}) => `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${isActive ? 'bg-emerald-500/15 text-white' : 'text-slate-400 hover:bg-white/[.06] hover:text-white'}`}>
                <Icon size={17}/><span>{label}</span>
              </NavLink>
            ))}
          </nav>
          <div className="border-t border-white/10 p-3">
            <div className="mb-2 rounded-xl bg-white/[.05] p-3">
              <p className="truncate text-sm font-medium">{user?.name || 'User'}</p>
              <p className="mt-1 text-xs text-emerald-200/50">{user?.role_name?.replaceAll('_',' ')}</p>
            </div>
            <button onClick={async()=>{await logout();navigate('/login')}} className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 hover:bg-white/[.06] hover:text-white">
              <LogOut size={17}/> Sign out
            </button>
          </div>
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex h-[72px] items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
            <div>
              <p className="text-xs font-medium uppercase tracking-wider text-emerald-600">{title}</p>
              <h1 className="text-lg font-semibold text-slate-900">{user?.name || 'Welcome'}</h1>
            </div>
            <div className="flex items-center gap-3">
              <span className="hidden rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium capitalize text-emerald-700 sm:block">{user?.role_name?.replaceAll('_',' ')}</span>
              <button onClick={async()=>{await logout();navigate('/login')}} className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50 lg:hidden"><LogOut size={17}/></button>
            </div>
          </header>
          <main className="flex-1 px-4 py-5 sm:px-6 lg:px-8">
            <div className="mx-auto w-full max-w-[1500px]"><Outlet/></div>
          </main>
        </div>
      </div>
    </div>
  )
}
