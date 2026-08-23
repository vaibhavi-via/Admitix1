export default function FormField({
  field,
  value,
  onChange,
  error,
}) {
  const {
    name,
    label,
    type = 'text',
    required,
    options,
    placeholder,
    helpText,
    readOnly,
    format,
    loading,
    disabled,
  } = field

  const inputId = `field-${name}`

  const baseInputClass = `
    w-full rounded-xl border bg-white px-3.5 py-2.5
    text-sm text-slate-900
    placeholder:text-slate-400
    outline-none transition-all duration-150
    disabled:cursor-not-allowed
    disabled:bg-slate-50
    disabled:text-slate-500
    ${
      error
        ? 'border-red-300 focus:border-red-500 focus:ring-4 focus:ring-red-50'
        : 'border-slate-200 hover:border-slate-300 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50'
    }
  `

  if (type === 'checkbox') {
    return (
      <div className="rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-3.5 transition hover:bg-slate-50">
        <label
          htmlFor={inputId}
          className="!mb-0 flex cursor-pointer items-center gap-3"
        >
          <input
            id={inputId}
            type="checkbox"
            checked={!!value}
            disabled={readOnly || disabled}
            onChange={(e) => onChange(name, e.target.checked)}
            className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
          />
          <span className="text-sm font-semibold text-slate-700">{label}</span>
        </label>
      </div>
    )
  }

  return (
    <div>
      <label htmlFor={inputId} className="mb-1.5 block text-sm font-semibold text-slate-700">
        {label}
        {required && <span className="ml-1 text-red-500">*</span>}
      </label>

      {type === 'textarea' && (
        <textarea
          id={inputId}
          rows={4}
          value={value ?? ''}
          placeholder={placeholder}
          disabled={readOnly || disabled}
          onChange={(e) => onChange(name, e.target.value)}
          className={`${baseInputClass} resize-y`}
        />
      )}

      {type === 'select' && (
        <select
          id={inputId}
          value={value ?? ''}
          disabled={readOnly || disabled || loading}
          onChange={(e) => onChange(name, e.target.value)}
          className={baseInputClass}
        >
          <option value="">
            {loading ? 'Loading options...' : placeholder || 'Select...'}
          </option>
          {options?.map((opt) => {
            const option = typeof opt === 'object' ? opt : { value: opt, label: opt }
            return (
              <option key={option.value} value={option.value} disabled={option.disabled}>
                {option.label}
              </option>
            )
          })}
        </select>
      )}

      {!['textarea', 'select', 'checkbox'].includes(type) && (
        <input
          id={inputId}
          type={type}
          value={value ?? ''}
          placeholder={placeholder ?? (format === 'uuid' ? 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' : undefined)}
          disabled={readOnly || disabled}
          autoComplete={format === 'uuid' ? 'off' : undefined}
          onChange={(e) => onChange(name, e.target.value)}
          className={baseInputClass}
        />
      )}

      {helpText && !error && <p className="mt-1.5 text-xs leading-5 text-slate-400">{helpText}</p>}
      {error && <p className="mt-1.5 text-xs font-medium text-red-600">{error}</p>}
    </div>
  )
}
