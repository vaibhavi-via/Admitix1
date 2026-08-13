"""The `dashboard` module has no table of its own.

It aggregates data across `institutions`, `applications`,
`admission_cycles`, `payments`, `seat_matrix`, etc. for
summary/analytics views. Its `repository.py`/`service.py` query the
existing ORM models from other modules directly; no new SQLAlchemy
model belongs here.
"""

from __future__ import annotations
