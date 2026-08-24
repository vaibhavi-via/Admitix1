import { useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { CheckCircle2, KeyRound, MailCheck, RefreshCw } from 'lucide-react'
import { requestStaffOtp, verifyStaffOtp } from '../features/auth/services'

export default function ActivateAccount() {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [form, setForm] = useState({ email: '', institution_code: '', otp: '', password: '', confirm: '' })
  const [challengeToken, setChallengeToken] = useState('')
  const [devOtp, setDevOtp] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const update = (name, value) => setForm((prev) => ({ ...prev, [name]: value }))
  const canRequest = form.email.trim() && form.institution_code.trim()
  const canVerify = useMemo(
    () => challengeToken && /^\d{6}$/.test(form.otp) && form.password.length >= 8 && form.password === form.confirm,
    [challengeToken, form.otp, form.password, form.confirm],
  )

  const requestOtp = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')
    if (!canRequest) return setError('Enter your staff email and institution code.')
    setLoading(true)
    try {
      const data = await requestStaffOtp({ email: form.email.trim(), institution_code: form.institution_code.trim() })
      setChallengeToken(data.challenge_token)
      setDevOtp(data.dev_otp || '')
      setMessage(data.message || 'OTP sent. Check your email.')
      setStep(2)
    } catch (err) {
      setError(err.message || 'Could not send OTP.')
    } finally {
      setLoading(false)
    }
  }

  const verify = async (event) => {
    event.preventDefault()
    setError('')
    if (!canVerify) return setError('Enter the 6-digit OTP and a matching password of at least 8 characters.')
    setLoading(true)
    try {
      const data = await verifyStaffOtp({
        email: form.email.trim(),
        institution_code: form.institution_code.trim(),
        otp: form.otp,
        challenge_token: challengeToken,
        new_password: form.password,
      })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify({
        ...data.user,
        name: [data.user.first_name, data.user.last_name].filter(Boolean).join(' '),
      }))
      navigate('/officer', { replace: true })
    } catch (err) {
      setError(err.message || 'OTP verification failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
          {step === 1 ? <MailCheck size={20} /> : <KeyRound size={20} />}
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Activate staff account</h1>
        <p className="mt-2 text-sm leading-5 text-slate-500">
          {step === 1 ? 'Use the email and institution code given by your administrator.' : 'Verify the OTP and set your new password.'}
        </p>
      </div>

      {step === 1 ? (
        <form onSubmit={requestOtp} className="space-y-5">
          <div>
            <label htmlFor="email">Staff email address</label>
            <input id="email" type="email" value={form.email} onChange={(e) => update('email', e.target.value)} placeholder="officer@example.com" autoComplete="email" />
          </div>
          <div>
            <label htmlFor="institution_code">Institution code</label>
            <input id="institution_code" value={form.institution_code} onChange={(e) => update('institution_code', e.target.value.toUpperCase())} placeholder="e.g. ABCENG" autoComplete="off" />
          </div>
          {error && <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">{error}</div>}
          <button disabled={loading} className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white hover:bg-emerald-700 disabled:opacity-60">
            {loading ? 'Sending OTP…' : 'Send OTP'}
          </button>
        </form>
      ) : (
        <form onSubmit={verify} className="space-y-5">
          {message && <div className="rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{message}</div>}
          {devOtp && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
              <b>Local demo OTP:</b> {devOtp}
              <p className="mt-1 text-xs">This appears because SMTP is not configured. In production, the OTP is delivered by email.</p>
            </div>
          )}
          <div>
            <label htmlFor="otp">6-digit OTP</label>
            <input id="otp" inputMode="numeric" maxLength={6} value={form.otp} onChange={(e) => update('otp', e.target.value.replace(/\D/g, '').slice(0, 6))} placeholder="123456" autoComplete="one-time-code" />
          </div>
          <div>
            <label htmlFor="password">New password</label>
            <input id="password" type="password" value={form.password} onChange={(e) => update('password', e.target.value)} minLength={8} autoComplete="new-password" placeholder="At least 8 characters" />
          </div>
          <div>
            <label htmlFor="confirm">Confirm password</label>
            <input id="confirm" type="password" value={form.confirm} onChange={(e) => update('confirm', e.target.value)} minLength={8} autoComplete="new-password" placeholder="Re-enter your password" />
          </div>
          {error && <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">{error}</div>}
          <div className="grid gap-2 sm:grid-cols-2">
            <button type="button" onClick={() => { setStep(1); setError(''); setMessage(''); setDevOtp('') }} className="rounded-xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700">Change email</button>
            <button disabled={loading} className="flex items-center justify-center gap-2 rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white hover:bg-emerald-700 disabled:opacity-60">
              {loading ? 'Activating…' : <><CheckCircle2 size={17} /> Verify & activate</>}
            </button>
          </div>
          <button type="button" disabled={loading} onClick={requestOtp} className="flex w-full items-center justify-center gap-2 text-sm font-semibold text-emerald-600 hover:text-emerald-700 disabled:opacity-50">
            <RefreshCw size={15} /> Send a new OTP
          </button>
        </form>
      )}

      <p className="mt-7 text-center text-sm text-slate-500">
        Already activated? <Link to="/login" className="font-semibold text-emerald-600">Back to sign in</Link>
      </p>
    </div>
  )
}
