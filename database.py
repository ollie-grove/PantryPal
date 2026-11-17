
import sqlite3
from pathlib import Path

# Create a folder for our database
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "pantry.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                category TEXT,
                expiration_date TEXT,
                notes TEXT
            )
        """)


def add_item(name, location, quantity, unit, category,
             expiration_date, notes):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO inventory
            (name, location, quantity, unit, category,
             expiration_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name, location, quantity, unit, category,
            expiration_date, notes
        ))


def get_all_items():
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM inventory ORDER BY name
        """).fetchall()


def update_item(item_id, name, location, quantity, unit,
                category, expiration_date, notes):
    with get_connection() as conn:
        conn.execute("""
            UPDATE inventory
            SET name=?, location=?, quantity=?, unit=?,
                category=?, expiration_date=?, notes=?
            WHERE id=?
        """, (
            name, location, quantity, unit, category,
            expiration_date, notes, item_id
        ))


def delete_item(item_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM inventory WHERE id=?",
            (item_id,)
        )
