import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })

  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!form.name || !form.email || !form.password || !form.confirmPassword) {
      setError('Please fill in all fields.')
      return
    }

    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.')
      return
    }

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setIsSubmitting(true)

    try {
      // Mock registration for now.
      // Once backend registration is ready, this will call the API.
      await login({
        email: form.email,
        password: form.password,
      })

      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err.message || 'Could not create your account.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <h1 className="text-xl font-semibold text-gray-900">
        Create your account
      </h1>

      <p className="mb-6 mt-1 text-sm text-gray-500">
        Register to access the Admitix administration portal.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name">Full name</label>

          <input
            id="name"
            name="name"
            type="text"
            value={form.name}
            onChange={handleChange}
            placeholder="Your full name"
          />
        </div>

        <div>
          <label htmlFor="email">Email</label>

          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={handleChange}
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>

          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            value={form.password}
            onChange={handleChange}
            placeholder="Minimum 6 characters"
          />
        </div>

        <div>
          <label htmlFor="confirmPassword">Confirm password</label>

          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            autoComplete="new-password"
            value={form.confirmPassword}
            onChange={handleChange}
            placeholder="Re-enter your password"
          />
        </div>

        {error && (
          <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? 'Creating account...' : 'Create account'}
        </button>
      </form>

      <p className="mt-5 text-center text-sm text-gray-500">
        Already have an account?{' '}
        <Link
          to="/login"
          className="font-semibold text-emerald-600 hover:text-emerald-700"
        >
          Sign in
        </Link>
      </p>
    </>
  )
}