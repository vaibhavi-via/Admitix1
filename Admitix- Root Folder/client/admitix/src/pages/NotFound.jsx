import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 p-6 text-center">
      <p className="text-5xl font-bold text-indigo-600">404</p>
      <h1 className="text-xl font-semibold text-gray-900">Page not found</h1>
      <p className="max-w-sm text-gray-500">
        The page you're looking for doesn't exist or may have been moved.
      </p>
      <Link
        to="/dashboard"
        className="mt-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-indigo-700"
      >
        Back to dashboard
      </Link>
    </div>
  )
}
