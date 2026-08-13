 import { Outlet } from 'react-router-dom'
import { GraduationCap, ShieldCheck, Sparkles } from 'lucide-react'
import { APP_NAME } from '../utils/constants'

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* Left branding panel */}
        <div className="relative hidden overflow-hidden bg-[#0B2117] lg:flex lg:flex-col lg:justify-between p-10 xl:p-14">
          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />
          <div className="absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl" />

          {/* Logo */}
          <div className="relative flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500 shadow-lg shadow-emerald-500/20">
              <GraduationCap size={23} className="text-white" />
            </div>

            <div>
              <p className="text-lg font-bold tracking-wide text-white">
                {APP_NAME}
              </p>
              <p className="text-xs text-emerald-200/60">
                Administration Portal
              </p>
            </div>
          </div>

          {/* Main message */}
          <div className="relative max-w-xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-xs font-medium text-emerald-300">
              <Sparkles size={13} />
              Smarter admissions management
            </div>

            <h1 className="text-4xl font-bold leading-tight text-white xl:text-5xl">
              Manage your entire
              <span className="block text-emerald-400">
                admission ecosystem.
              </span>
            </h1>

            <p className="mt-5 max-w-lg text-sm leading-6 text-slate-400">
              Manage institutions, faculties, departments, courses,
              students and applications from one centralized platform.
            </p>

            <div className="mt-8 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 text-emerald-400">
                <ShieldCheck size={19} />
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  Secure administration
                </p>
                <p className="text-xs text-slate-500">
                  Built for modern educational institutions
                </p>
              </div>
            </div>
          </div>

          <p className="relative text-xs text-slate-600">
            © {new Date().getFullYear()} {APP_NAME}
          </p>
        </div>

        {/* Login area */}
        <div className="flex min-h-screen items-center justify-center px-5 py-10 sm:px-8">
          <div className="w-full max-w-md">
            {/* Mobile logo */}
            <div className="mb-10 flex items-center gap-3 lg:hidden">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600 text-white shadow-lg shadow-emerald-600/20">
                <GraduationCap size={21} />
              </div>

              <div>
                <p className="font-bold text-slate-900">
                  {APP_NAME}
                </p>
                <p className="text-[11px] text-slate-400">
                  Administration Portal
                </p>
              </div>
            </div>

            <Outlet />
          </div>
        </div>

      </div>
    </div>
  )
}
