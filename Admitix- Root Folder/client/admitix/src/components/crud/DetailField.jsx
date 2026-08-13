// One label/value pair on a module's Details page.
function isUUID(value) {
  return typeof value === 'string' &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value)
}

export default function DetailField({ label, value }) {
  // Internal UUIDs are deliberately not rendered in user-facing details.
  if (isUUID(value)) return null

  let display = value
  if (typeof value === 'boolean') display = value ? 'Yes' : 'No'
  if (value === '' || value === null || value === undefined) display = '—'

  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-400">{label}</dt>
      <dd className="mt-1 text-sm text-gray-900 break-words">{String(display)}</dd>
    </div>
  )
}
