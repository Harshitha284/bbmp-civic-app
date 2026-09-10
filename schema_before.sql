-- CivicLens complaints table — ORIGINAL schema
-- Problem: nothing stops the same complaint being inserted twice
-- (e.g. a user double-clicks "Submit", or the app retries on a slow
-- network). Also, filtering complaints by ward does a full table scan
-- once the table grows, since there's no index on ward_id.

CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ward_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    created_at TEXT NOT NULL
);
