// One label/value pair on a module's Details page.
export default function DetailField({ label, value }) {
  let display = value
  if (typeof value === 'boolean') display = value ? 'Yes' : 'No'
  if (value === '' || value === null || value === undefined) display = '—'

  const text = String(display)
  const isRawId = text.length > 20 && /^[0-9a-f-]+$/i.test(text)

  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-gray-400">{label}</dt>
      <dd
        className="mt-1 break-words text-sm text-gray-900"
        title={isRawId ? text : undefined}
      >
        {isRawId ? (
          <span className="font-mono text-xs text-slate-500">{text.slice(0, 8)}...</span>
        ) : (
          text
        )}
      </dd>
    </div>
  )
}
