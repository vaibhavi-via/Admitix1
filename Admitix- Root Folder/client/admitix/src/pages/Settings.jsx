import { useAuth } from '../context/AuthContext'

export default function Settings() {
  const { user } = useAuth()

  return (
    <div>
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Settings</h1>
      <div className="max-w-md rounded-xl border border-gray-200 bg-white p-6">
        <div className="mb-4">
          <label>Name</label>
          <input value={user?.name || ''} disabled />
        </div>
        <div className="mb-4">
          <label>Email</label>
          <input value={user?.email || ''} disabled />
        </div>
        <p className="text-xs text-gray-500">
          Wire this form up to your profile-update endpoint when it's ready.
        </p>
      </div>
    </div>
  )
}
