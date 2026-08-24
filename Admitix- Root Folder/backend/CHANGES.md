# Admitix backend — changes in this pass

All changes are additive: no existing model, schema, or endpoint was
removed or had its contract changed. Every new relationship is nullable,
so existing rows/institutions continue to work with no forced backfill.

## New: `domains` module (mirrors the existing `roles` module exactly)
`modules/domains/` — model, schema, service, router, repository,
exceptions, permissions, dependencies, constants, validators.

Endpoints (all behind the same auth dependency as every other module):
- `POST   /domains/`
- `GET    /domains/`
- `GET    /domains/{domain_id}`
- `PATCH  /domains/{domain_id}`
- `DELETE /domains/{domain_id}`

Registered in `app/router.py` and `db/base.py` (metadata registration, same
pattern as every other model).

## Institutions are now domain-specific
- `modules/institutions/models.py` — added `domain_id` (nullable UUID FK to
  `domains.domain_id`, `ON DELETE RESTRICT` — matches the intent in your
  original SQL file) and the `domain` relationship.
- `modules/institutions/schema.py` — added `domain_id: uuid.UUID | None` to
  `InstitutionBase` and `InstitutionUpdate`, so it flows through create,
  update, and read automatically.

## Seed data
- `db/seed.py` — now also seeds the four domains (Engineering, Medical,
  Law, Pharmacy) alongside the existing role/super-admin seeding, so a
  fresh environment has the dropdown populated immediately.

## SQL to run on your existing local database
`db/migrations/manual/2026_08_23_domains_and_cleanup.sql`

This replaces the broken tail of the schema file you originally shared
(which had a self-contradicting `SET NOT NULL` / `DROP NOT NULL`, a couple
of stray `SELECT`s referencing columns that don't exist on `institutions`,
and a plaintext `ALTER USER postgres WITH PASSWORD ...`). It is idempotent
— safe to run whether your DB already partially ran the old script or
never has. It does **not** repeat the password change; see the note at
the bottom of that file about rotating your postgres password since it
was exposed in plaintext in the file you shared.

## Verified
- Every new/changed Python file parses cleanly.
- The FastAPI app imports successfully end-to-end and
  `sqlalchemy.orm.configure_mappers()` succeeds (this is what would catch
  a broken relationship/foreign key at import time) — confirmed the new
  `/domains/` and `/domains/{domain_id}` routes are registered in the
  OpenAPI schema alongside all 26 existing modules (71 total paths).

## 2026-08-24 – Staff activation, officer RBAC and dashboard hardening
- Added admin-only staff account creation with `admission_officer` role support.
- Added 48-hour staff activation token flow and `/auth/activate` password setup endpoint.
- Enforced role-based permissions at the API router level for admin, admission officer and student access.
- Added tenant/ownership checks for students, applications, documents, educational details, entrance scores, preferences, payments and notifications.
- Restricted admission officers to assigned applications/documents/payments while retaining admission workflow access.
- Scoped officer dashboard statistics and payment summaries to assigned applications.
- Kept database schema unchanged; no migration is required for these changes.
