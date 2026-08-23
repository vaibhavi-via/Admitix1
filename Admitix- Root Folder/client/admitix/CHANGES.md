# Admitix frontend — changes in this pass

All changes are additive/generic-component-level so every existing page keeps
working exactly as before; nothing was removed and no API contracts changed.

## 1. UUIDs are no longer shown raw to users
- `src/components/crud/DataTable.jsx` — every column (not just the first) now
  detects raw UUID-looking values and shows a truncated, copyable chip
  instead of the full id.
- `src/components/crud/DetailField.jsx` — same treatment on every module's
  "View details" page.

## 2. Foreign-key fields are now dropdowns, everywhere, automatically
- New hook: `src/hooks/useAutoRelationFields.js`
- Wired once into `src/components/crud/EntityForm.jsx`
- Any Create/Edit field whose name matches a known foreign key
  (`student_id`, `course_id`, `reviewed_by`, `domain_id`, ...) is now
  automatically converted from a raw-UUID text box into a searchable
  dropdown of real, human-readable records (name/code instead of a UUID),
  using the endpoints already defined in
  `src/components/crud/relationOptions.js`.
- Pages that already did their own bespoke, filtered dropdown wiring
  (Departments, Faculties) are untouched — the hook only acts on fields
  that don't already have options.
- Added a couple of missing relation mappings that existed as raw UUID
  boxes before: `reviewed_by`, `verified_by`, `changed_by` (all → Users),
  and the new `domain_id` (→ Domains).

## 3. Institutions are now domain-specific
- `src/features/institutions/constants.js` — added a `domain_id` field
  (dropdown: Engineering / Medical / Law / Pharmacy / ...), backed by the
  new `/domains` backend endpoint (see backend changes).
- `src/features/institutions/pages/InstitutionsListPage.jsx` — the
  Institutions list now shows the resolved domain name as a badge instead
  of a raw UUID.

## 4. Sidebar height
- `src/components/Sidebar.jsx` — the six navigation groups are now a
  collapsible accordion. Only one group is expanded at a time (the one
  containing your current page, by default), so the sidebar no longer
  scrolls through every link in every module at once.

## 5. Login page polish
- `src/pages/Login.jsx` — fixed the institution-code field, which was
  missing the same spacing/label styling as the email and password
  fields, and added a short helper line under it.
- The existing `AuthLayout.jsx` branding panel (left-hand "Manage your
  entire admission ecosystem" panel) was already a solid landing screen
  for login and was left as-is.

## Not changed (would need a larger, riskier pass)
- Per-row column customization beyond the Institutions list (i.e. showing
  a resolved name instead of a truncated id in every list, not just a
  copyable chip) — doable, but each of the ~20 list pages would need its
  own `render` function; happy to do this next if useful.
