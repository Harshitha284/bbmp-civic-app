"""
Demonstrates a real duplicate-complaint bug in CivicLens's data layer,
and the fix.

Problem observed:
    A user double-clicking "Submit" on the complaint form (or the app
    retrying a request on a slow connection) could insert the exact
    same complaint into the database twice. The original schema had
    no constraint to catch this, so duplicates silently piled up and
    inflated complaint counts on the BBMP dashboard.

Fix:
    Added a UNIQUE constraint on (user_id, description, created_at) so
    the database itself rejects an exact repeat submission, plus an
    index on ward_id so the staff dashboard's per-ward complaint
    lookup doesn't do a full table scan as the table grows.

Run:
    python demo_duplicate_bug.py
"""

import sqlite3


def load_schema(conn: sqlite3.Connection, schema_path: str) -> None:
    with open(schema_path) as f:
        conn.executescript(f.read())


def try_insert_duplicate(conn: sqlite3.Connection) -> str:
    """Simulate a double-click: the exact same complaint submitted twice."""
    complaint = (101, 7, "Streetlight not working near 5th cross", "Electrical", "2026-05-24 10:00:00")

    conn.execute(
        "INSERT INTO complaints (user_id, ward_id, description, category, created_at) VALUES (?, ?, ?, ?, ?)",
        complaint,
    )
    conn.commit()

    try:
        conn.execute(
            "INSERT INTO complaints (user_id, ward_id, description, category, created_at) VALUES (?, ?, ?, ?, ?)",
            complaint,
        )
        conn.commit()
        return "DUPLICATE INSERTED — bug present"
    except sqlite3.IntegrityError:
        return "duplicate REJECTED — fix working"


def main() -> None:
    print("=== BEFORE: original schema ===")
    before = sqlite3.connect(":memory:")
    load_schema(before, "schema_before.sql")
    print(try_insert_duplicate(before))
    count = before.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    print(f"Rows in complaints table after double-submit: {count}  (expected 1)\n")

    print("=== AFTER: fixed schema ===")
    after = sqlite3.connect(":memory:")
    load_schema(after, "schema_after.sql")
    print(try_insert_duplicate(after))
    count = after.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    print(f"Rows in complaints table after double-submit: {count}  (expected 1)")


if __name__ == "__main__":
    main()
