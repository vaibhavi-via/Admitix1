 import { useState } from 'react'
import {
  Menu,
  LogOut,
  ChevronDown,
  Bell,
  Search,
  User,
  Settings,
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useLocation, useNavigate } from 'react-router-dom'

const PAGE_TITLES = {
  '/dashboard': 'Dashboard',
  '/institutions': 'Institutions',
  '/faculties': 'Faculties',
  '/departments': 'Departments',
  '/courses': 'Courses',
  '/admission-cycles': 'Admission Cycles',
  '/seat-matrix': 'Seat Matrix',
  '/users': 'Users',
  '/roles': 'Roles',
  '/staff': 'Staff',
  '/students': 'Students',
  '/educational-details': 'Educational Details',
  '/entrance-exam-scores': 'Entrance Exam Scores',
  '/applications': 'Applications',
  '/application-preferences': 'Application Preferences',
  '/application-status-history': 'Status History',
  '/document-types': 'Document Types',
  '/documents': 'Documents',
  '/ai-verification': 'AI Verification',
  '/fee-structure': 'Fee Structure',
  '/payments': 'Payments',
  '/notifications': 'Notifications',
  '/chat': 'Chat History',
  '/reports': 'Reports',
  '/audit-logs': 'Audit Logs',
  '/settings': 'Settings',
}

export default function Navbar({ onMenuClick }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [menuOpen, setMenuOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)

  const handleLogout = () => {
    setMenuOpen(false)
    logout()
    navigate('/login')
  }

  const initials = (user?.name || 'User')
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()

  const pageTitle =
    PAGE_TITLES[location.pathname] ||
    Object.entries(PAGE_TITLES).find(([path]) =>
      location.pathname.startsWith(`${path}/`),
    )?.[1] ||
    'Admitix'

  return (
    <header
      className="
        sticky top-0 z-20
        flex h-[72px] shrink-0 items-center
        border-b border-slate-200
        bg-white/95 px-4
        backdrop-blur-xl
        sm:px-6
      "
    >
      {/* Mobile menu */}
      <button
        onClick={onMenuClick}
        aria-label="Open menu"
        className="
          mr-3 flex h-10 w-10 items-center justify-center
          rounded-xl text-slate-500
          transition
          hover:bg-emerald-50
          hover:text-emerald-700
          lg:hidden
        "
      >
        <Menu size={21} />
      </button>

      {/* Page title */}
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <span className="hidden h-2 w-2 rounded-full bg-emerald-500 sm:block" />

          <h1 className="truncate text-[17px] font-bold tracking-tight text-slate-900">
            {pageTitle}
          </h1>
        </div>

        <p className="mt-0.5 hidden text-[11px] font-medium text-slate-400 sm:block">
          Admitix Administration Portal
        </p>
      </div>

      {/* Right section */}
      <div className="ml-auto flex items-center gap-1.5 sm:gap-2">

        {/* Search */}
        <div className="relative">
          {searchOpen ? (
            <div
              className="
                flex h-10 items-center
                rounded-xl
                border border-emerald-200
                bg-emerald-50/40
                px-3
                shadow-sm
                ring-2 ring-emerald-50
              "
            >
              <Search size={16} className="text-emerald-600" />

              <input
                autoFocus
                type="text"
                placeholder="Search..."
                className="
                  !w-32
                  !border-0
                  !bg-transparent
                  !p-0
                  !pl-2
                  !text-sm
                  !text-slate-700
                  !outline-none
                  !shadow-none
                  !ring-0
                  placeholder:!text-slate-400
                  sm:!w-48
                "
                onBlur={() => setSearchOpen(false)}
              />
            </div>
          ) : (
            <button
              onClick={() => setSearchOpen(true)}
              aria-label="Search"
              className="
                flex h-10 w-10 items-center justify-center
                rounded-xl
                text-slate-500
                transition
                hover:bg-emerald-50
                hover:text-emerald-700
              "
            >
              <Search size={19} strokeWidth={1.8} />
            </button>
          )}
        </div>

        {/* Notifications */}
        <button
          aria-label="Notifications"
          onClick={() => navigate('/notifications')}
          className="
            relative flex h-10 w-10 items-center justify-center
            rounded-xl
            text-slate-500
            transition
            hover:bg-emerald-50
            hover:text-emerald-700
          "
        >
          <Bell size={19} strokeWidth={1.8} />

          <span
            className="
              absolute right-2.5 top-2
              h-2 w-2 rounded-full
              bg-emerald-500
              ring-2 ring-white
            "
          />
        </button>

        {/* Divider */}
        <div className="mx-1 hidden h-8 w-px bg-slate-200 sm:block" />

        {/* User menu */}
        <div className="relative">
          <button
            onClick={() => setMenuOpen((value) => !value)}
            className="
              flex items-center gap-2
              rounded-xl
              px-1.5 py-1.5
              transition
              hover:bg-slate-50
            "
          >
            {/* Avatar */}
            <span
              className="
                flex h-9 w-9 items-center justify-center
                rounded-full
                bg-gradient-to-br from-emerald-500 to-emerald-700
                text-xs font-bold text-white
                shadow-md shadow-emerald-600/20
                ring-2 ring-emerald-50
              "
            >
              {initials}
            </span>

            {/* User details */}
            <span className="hidden text-left sm:block">
              <span className="block max-w-[130px] truncate text-sm font-semibold text-slate-700">
                {user?.name || 'Guest'}
              </span>

              <span className="block text-[11px] font-medium text-slate-400">
                Administrator
              </span>
            </span>

            <ChevronDown
              size={16}
              className={`
                hidden text-slate-400 transition-transform
                sm:block
                ${menuOpen ? 'rotate-180 text-emerald-600' : ''}
              `}
            />
          </button>

          {/* Dropdown */}
          {menuOpen && (
            <>
              <div
                className="fixed inset-0 z-30"
                onClick={() => setMenuOpen(false)}
              />

              <div
                className="
                  absolute right-0 top-full z-40 mt-2
                  w-60 overflow-hidden
                  rounded-2xl
                  border border-slate-200
                  bg-white
                  shadow-xl shadow-slate-900/10
                "
              >
                {/* User information */}
                <div className="bg-gradient-to-br from-emerald-50 to-white px-4 py-4">
                  <div className="flex items-center gap-3">
                    <span
                      className="
                        flex h-10 w-10 shrink-0 items-center justify-center
                        rounded-full
                        bg-gradient-to-br from-emerald-500 to-emerald-700
                        text-xs font-bold text-white
                        shadow-sm
                      "
                    >
                      {initials}
                    </span>

                    <div className="min-w-0">
                      <p className="truncate text-sm font-bold text-slate-800">
                        {user?.name || 'Guest'}
                      </p>

                      <p className="mt-0.5 truncate text-xs text-slate-400">
                        {user?.email || 'Administrator'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Menu */}
                <div className="p-1.5">

                  {/* Profile */}
                  <button
                    onClick={() => {
                      setMenuOpen(false)
                      navigate('/settings')
                    }}
                    className="
                      flex w-full items-center gap-3
                      rounded-xl
                      px-3 py-2.5
                      text-sm text-slate-600
                      transition
                      hover:bg-emerald-50
                      hover:text-emerald-700
                    "
                  >
                    <span
                      className="
                        flex h-8 w-8 items-center justify-center
                        rounded-lg
                        bg-slate-100
                        text-slate-500
                      "
                    >
                      <User size={16} />
                    </span>

                    <span>Profile & Settings</span>
                  </button>

                  {/* Settings */}
                  <button
                    onClick={() => {
                      setMenuOpen(false)
                      navigate('/settings')
                    }}
                    className="
                      flex w-full items-center gap-3
                      rounded-xl
                      px-3 py-2.5
                      text-sm text-slate-600
                      transition
                      hover:bg-emerald-50
                      hover:text-emerald-700
                    "
                  >
                    <span
                      className="
                        flex h-8 w-8 items-center justify-center
                        rounded-lg
                        bg-slate-100
                        text-slate-500
                      "
                    >
                      <Settings size={16} />
                    </span>

                    <span>Settings</span>
                  </button>

                  <div className="my-1.5 border-t border-slate-100" />

                  {/* Logout */}
                  <button
                    onClick={handleLogout}
                    className="
                      flex w-full items-center gap-3
                      rounded-xl
                      px-3 py-2.5
                      text-sm text-red-600
                      transition
                      hover:bg-red-50
                    "
                  >
                    <span
                      className="
                        flex h-8 w-8 items-center justify-center
                        rounded-lg
                        bg-red-50
                      "
                    >
                      <LogOut size={16} />
                    </span>

                    <span className="font-medium">Log out</span>
                  </button>

                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  )
}