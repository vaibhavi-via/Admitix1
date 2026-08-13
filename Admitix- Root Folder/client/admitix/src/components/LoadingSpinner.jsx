export default function LoadingSpinner({ fullScreen = false, label = 'Loading…' }) {
  return (
    <div
      className={
        fullScreen
          ? 'flex min-h-screen flex-col items-center justify-center gap-3'
          : 'flex flex-col items-center justify-center gap-3 py-6'
      }
    >
      <div
        role="status"
        aria-label={label}
        className="h-8 w-8 animate-spin rounded-full border-2 border-gray-200 border-t-indigo-600"
      />
      {label && <p className="text-sm text-gray-500">{label}</p>}
    </div>
  )
}
