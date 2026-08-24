import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Eye, EyeOff, ArrowRight, LockKeyhole } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const from = location.state?.from?.pathname || '/'

  const [form, setForm] = useState({
    email: '',
    password: '',
    institution_code: '',
  })

  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!form.email || !form.password || !form.institution_code) {
      setError('Enter your institution code, email and password to continue.')
      return
    }

    setIsSubmitting(true)

    try {
      await login(form)
      navigate(from, { replace: true })
    } catch (err) {
      setError(
        err.message || 'Could not log in. Check your credentials.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div>
      {/* Heading */}
      <div className="mb-8">
        <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
          <LockKeyhole size={20} />
        </div>

        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Welcome back
        </h1>

        <p className="mt-2 text-sm leading-5 text-slate-500">
          Sign in to access your administration dashboard.
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-5">

        <div>
          <label htmlFor="institution_code">Institution code</label>
          <input
            id="institution_code"
            name="institution_code"
            value={form.institution_code}
            onChange={handleChange}
            placeholder="e.g. ABCENG"
            autoComplete="off"
          />
          <p className="mt-1.5 text-xs leading-5 text-slate-400">
            The unique code your institution was registered with.
          </p>
        </div>

        <div>
          <label htmlFor="email">
            Email address
          </label>

          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={handleChange}
            placeholder="admin@example.com"
          />
        </div>

        <div>
          <div className="mb-1.5 flex items-center justify-between">
            <label htmlFor="password" className="mb-0">
              Password
            </label>

            <button
              type="button"
              className="text-xs font-medium text-emerald-600 hover:text-emerald-700"
            >
              Forgot password?
            </button>
          </div>

          <div className="relative">
            <input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter your password"
              className="pr-11"
            />

            <button
              type="button"
              onClick={() => setShowPassword((value) => !value)}
              aria-label={
                showPassword
                  ? 'Hide password'
                  : 'Show password'
              }
              className="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            >
              {showPassword ? (
                <EyeOff size={17} />
              ) : (
                <Eye size={17} />
              )}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="group flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-600/15 transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? 'Signing in...' : 'Sign in'}

          {!isSubmitting && (
            <ArrowRight
              size={17}
              className="transition-transform group-hover:translate-x-0.5"
            />
          )}
        </button>
      </form>

<p className="mt-7 text-center text-sm text-gray-500">Don't have an account? <a href="/register" className="font-semibold text-emerald-600">Create account</a></p>
    </div>
  )
} 
