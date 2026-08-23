-- =====================================================================
-- ADMITIX — Manual SQL: domain-specific institutions (cleanup pass)
-- =====================================================================
-- Run this once against your existing local database.
--
-- WHY THIS FILE EXISTS
-- ---------------------------------------------------------------------
-- Your original schema file ended with a messy, exploratory tail:
--   * `domain_id` was added, then set NOT NULL, then immediately set
--     back to nullable again (contradicts itself — left as nullable).
--   * a handful of ad-hoc SELECT statements were left in the file,
--     including one referencing columns that don't exist on
--     `institutions` (`id`, `name`, `code`, `is_active` — the real
--     columns are `institution_id`, `institution_name`,
--     `institution_code`, `status`). Running the original file
--     top-to-bottom as-is would error out on that statement.
--   * `ALTER USER postgres WITH PASSWORD 'Vaibhavi1122';` set your
--     postgres superuser password IN PLAIN TEXT inside a script that
--     you're now sharing around. Please rotate that password — this
--     script deliberately does NOT repeat that statement.
--
-- This file is idempotent: safe to run whether your database already
-- ran the messy version of the script, or has never seen `domains`/
-- `domain_id` at all (e.g. a fresh DB built from the original 23-table
-- schema before that tail was added). Every step checks for existence
-- first, so re-running this file is also safe and won't error.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. Ensure the `domains` table exists (no-op if you already have it).
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS domains (
    domain_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_code   VARCHAR(20)  NOT NULL,
    domain_name   VARCHAR(100) NOT NULL,
    description   TEXT,
    status        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_domains_code UNIQUE (domain_code),
    CONSTRAINT uq_domains_name UNIQUE (domain_name)
);

INSERT INTO domains (domain_code, domain_name) VALUES
    ('ENG',   'Engineering'),
    ('MED',   'Medical'),
    ('LAW',   'Law'),
    ('PHARM', 'Pharmacy')
ON CONFLICT (domain_code) DO NOTHING;

-- ---------------------------------------------------------------------
-- 2. Ensure `institutions.domain_id` exists with the correct FK.
-- ---------------------------------------------------------------------
ALTER TABLE institutions
    ADD COLUMN IF NOT EXISTS domain_id UUID;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_name = 'fk_institutions_domain_id'
          AND table_name = 'institutions'
    ) THEN
        ALTER TABLE institutions
            ADD CONSTRAINT fk_institutions_domain_id
            FOREIGN KEY (domain_id) REFERENCES domains (domain_id) ON DELETE RESTRICT;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_institutions_domain_id ON institutions (domain_id);

-- ---------------------------------------------------------------------
-- 3. Best-effort backfill for any institution left without a domain,
--    using the same name-matching heuristic as your original script.
--    This only touches rows that are still NULL, so it's safe to
--    re-run and won't overwrite a domain you've already assigned
--    manually via the app.
-- ---------------------------------------------------------------------
UPDATE institutions
SET domain_id = (SELECT domain_id FROM domains WHERE domain_code = 'ENG')
WHERE domain_id IS NULL AND institution_name ILIKE '%engineering%';

UPDATE institutions
SET domain_id = (SELECT domain_id FROM domains WHERE domain_code = 'MED')
WHERE domain_id IS NULL AND institution_name ILIKE '%medical%';

UPDATE institutions
SET domain_id = (SELECT domain_id FROM domains WHERE domain_code = 'LAW')
WHERE domain_id IS NULL AND institution_name ILIKE '%law%';

UPDATE institutions
SET domain_id = (SELECT domain_id FROM domains WHERE domain_code = 'PHARM')
WHERE domain_id IS NULL AND institution_name ILIKE '%pharm%';

-- Deliberately left NULLABLE. A hard NOT NULL constraint here would
-- break every institution whose name doesn't match one of the four
-- heuristics above (or that hasn't been assigned a domain yet from
-- the UI). Assign remaining institutions a domain from the app's
-- Institution form — the new "Domain" dropdown added to the frontend
-- — then tighten this to NOT NULL yourself if/when every row has one:
--
--   ALTER TABLE institutions ALTER COLUMN domain_id SET NOT NULL;

COMMIT;

-- ---------------------------------------------------------------------
-- 4. Sanity check — run this yourself after the script finishes to see
--    which institutions (if any) still need a domain assigned by hand.
-- ---------------------------------------------------------------------
-- SELECT institution_id, institution_name, institution_code
-- FROM institutions
-- WHERE domain_id IS NULL;

-- =====================================================================
-- SECURITY NOTE
-- =====================================================================
-- Your previous script contained:
--   ALTER USER postgres WITH PASSWORD 'Vaibhavi1122';
-- That password is now sitting in a plaintext file. If this database
-- is anything other than a fully disposable local sandbox, rotate the
-- postgres user's password (and check it isn't reused anywhere else)
-- and set the new one via an environment variable / secrets manager
-- rather than a committed .sql file, e.g.:
--   ALTER USER postgres WITH PASSWORD 'a-new-password-you-store-safely';
-- =====================================================================
