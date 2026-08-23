// One label/value pair on a module's Details page.
export default function DetailField({ label, value }) {
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
