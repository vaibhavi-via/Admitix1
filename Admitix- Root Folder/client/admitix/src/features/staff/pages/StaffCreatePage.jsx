import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import { createStaffAccount } from '../services'

const initial = { first_name: '', last_name: '', email: '', phone: '', institution_id: '', department_id: '', employee_id: '', designation: 'Admission Officer', joining_date: '', role_name: 'admission_officer' }

export default function StaffCreatePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initial)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [created, setCreated] = useState(null)
  const set = (key, value) => setForm((current) => ({ ...current, [key]: value }))

  const submit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await createStaffAccount({ ...form, department_id: form.department_id || null, joining_date: form.joining_date || null })
      setCreated(data)
    } catch (err) {
      setError(err.message || 'Failed to create staff account.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <PageHeader title="Create Staff Account" subtitle="Create a pending admission officer account. The officer will verify their email with an OTP and set their own password." />
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        {!created ? (
          <form onSubmit={submit} className="grid gap-5 md:grid-cols-2">
            {Object.entries({ first_name: 'First name', last_name: 'Last name', email: 'Email', phone: 'Phone', institution_id: 'Institution ID', department_id: 'Department ID', employee_id: 'Employee ID', designation: 'Designation', joining_date: 'Joining date' }).map(([key, label]) => (
              <label key={key}>
                {label}
                <input type={key === 'email' ? 'email' : key === 'joining_date' ? 'date' : 'text'} value={form[key]} onChange={(e) => set(key, e.target.value)} required={!['last_name', 'phone', 'department_id', 'joining_date'].includes(key)} />
              </label>
            ))}
            {error && <div className="md:col-span-2 rounded-xl border border-red-100 bg-red-50 p-3 text-sm text-red-600">{error}</div>}
            <div className="md:col-span-2 flex justify-end gap-2">
              <button type="button" onClick={() => navigate('/staff')} className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold">Cancel</button>
              <button disabled={loading} className="rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white">{loading ? 'Creating…' : 'Create Staff Account'}</button>
            </div>
          </form>
        ) : (
          <div className="space-y-4">
            <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4 text-sm text-emerald-800">
              <b>Staff account created successfully.</b>
              <p className="mt-1">The account is pending activation. Give the officer the email and institution code. They can open the staff activation page, request an OTP, and set their password.</p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-xl bg-slate-50 p-4"><p className="text-xs text-slate-400">Staff email</p><p className="mt-1 font-semibold">{created.staff?.user?.email || form.email}</p></div>
              <div className="rounded-xl bg-slate-50 p-4"><p className="text-xs text-slate-400">Employee ID</p><p className="mt-1 font-semibold">{created.staff?.employee_id || form.employee_id}</p></div>
            </div>
            <div className="flex flex-wrap justify-end gap-2">
              <button onClick={() => navigate('/activate')} className="rounded-xl border border-emerald-200 px-5 py-2.5 text-sm font-semibold text-emerald-700">Open Activation Page</button>
              <button onClick={() => navigate('/staff')} className="rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white">Done</button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
