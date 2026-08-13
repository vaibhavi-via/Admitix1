// UUID validation used by relationship/foreign-key fields in CRUD forms.
// The backend remains the source of truth; this only prevents obviously
// malformed UUIDs from being submitted and gives the user a clear message.

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

export function isValidUUID(value) {
  return UUID_RE.test(String(value ?? '').trim())
}

export function normalizeUUID(value) {
  return typeof value === 'string' ? value.trim() : value
}
