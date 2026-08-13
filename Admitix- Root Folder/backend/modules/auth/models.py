"""The `auth` module has no dedicated table of its own.

Authentication operates directly on `modules.users.models.User`
(login, password hashing, `last_login` updates) and issues JWTs /
refresh tokens that are not persisted as their own table in this
schema. This file is kept (empty of ORM classes) purely so the module
still exposes `models.py`, consistent with every other module's
structure, and so `db.base` does not need special-casing for `auth`.

If refresh-token revocation/blacklisting is added later, its model
would live here.
"""

from __future__ import annotations
