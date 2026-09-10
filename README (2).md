# Database fix: duplicate complaint submissions

## Problem observed

CivicLens's original `complaints` table had no way to catch an exact
duplicate submission. If a user double-clicked "Submit," or the
client retried a request on a slow connection, the same complaint
(same user, same description, same timestamp) could be inserted
twice. This inflated complaint counts and duplicated work for BBMP
staff reviewing the queue.

Separately, the staff dashboard filters complaints by ward
(`WHERE ward_id = ?`) constantly. With no index on `ward_id`, this
does a full table scan on every request — fine at a handful of rows,
but it gets slower as complaints pile up.

## Fix

- `schema_before.sql` — the original schema (no dedup, no index)
- `schema_after.sql` — added a `UNIQUE (user_id, description, created_at)`
  constraint so the database rejects an exact repeat insert, plus an
  index on `ward_id` for faster per-ward lookups
- `demo_duplicate_bug.py` — a runnable script that loads both schemas
  into in-memory SQLite databases and proves the before/after behavior

## Run it yourself

```bash
cd db
python3 demo_duplicate_bug.py
```

Expected output: the "before" schema ends up with 2 rows after a
double-submit; the "after" schema stays at 1.
