-- CivicLens complaints table — FIXED schema
--
-- Fix 1: a UNIQUE constraint on (user_id, description, created_at)
-- rejects an exact-duplicate submission at the database level, so a
-- double-click or a client-side retry can no longer create two rows
-- for the same complaint.
--
-- Fix 2: an index on ward_id speeds up the ward-level lookup that the
-- BBMP staff dashboard runs constantly (WHERE ward_id = ?), instead of
-- scanning the whole table every time.

CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (user_id, description, created_at)
);

CREATE INDEX idx_complaints_ward_id ON complaints (ward_id);
