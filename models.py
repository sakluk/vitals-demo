"""
models.py — Tietokantatoiminnot VitalsDemo-sovellukselle.

Ei ORM:ää, suora sqlite3-kirjasto vaatimusmäärittelyn mukaisesti.
Yhteys haetaan Flaskin request-kontekstista (g) ja suljetaan
automaattisesti pyynnön päätteeksi (ks. app.py: teardown_appcontext).
"""

import sqlite3
from flask import current_app, g


def get_db():
    """Palauttaa nykyisen pyynnön SQLite-yhteyden, luoden sen tarvittaessa."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Sulkee tietokantayhteyden pyynnön päätteeksi."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --- Käyttäjät -------------------------------------------------------------

def get_user_by_username(username):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def get_user_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


def get_user_stats():
    """Montako mittausta ja huomiota kukin käyttäjä on kirjannut."""
    db = get_db()
    measurement_counts = db.execute(
        """
        SELECT recorded_by AS username, COUNT(*) AS count
        FROM measurements
        GROUP BY recorded_by
        """
    ).fetchall()
    note_counts = db.execute(
        """
        SELECT author AS username, COUNT(*) AS count
        FROM notes
        GROUP BY author
        """
    ).fetchall()
    return {
        "measurements": {row["username"]: row["count"] for row in measurement_counts},
        "notes": {row["username"]: row["count"] for row in note_counts},
    }


# --- Potilaat ----------------------------------------------------------------

def get_all_patients_with_latest():
    """Kaikki potilaat + viimeisimmän mittauksen aikaleima (jos on)."""
    db = get_db()
    rows = db.execute(
        """
        SELECT p.*, MAX(m.recorded_at) AS latest_measurement_at
        FROM patients p
        LEFT JOIN measurements m ON m.patient_id = p.id
        GROUP BY p.id
        ORDER BY p.name
        """
    ).fetchall()
    return rows


def get_patient(patient_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM patients WHERE id = ?", (patient_id,)
    ).fetchone()


def create_patient(name, dob, room):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO patients (name, dob, room, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """,
        (name, dob, room),
    )
    db.commit()
    return cur.lastrowid


def delete_patient(patient_id):
    db = get_db()
    db.execute("DELETE FROM measurements WHERE patient_id = ?", (patient_id,))
    db.execute("DELETE FROM notes WHERE patient_id = ?", (patient_id,))
    db.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    db.commit()


# --- Mittaukset --------------------------------------------------------------

def get_measurements_for_patient(patient_id):
    db = get_db()
    return db.execute(
        """
        SELECT * FROM measurements
        WHERE patient_id = ?
        ORDER BY recorded_at DESC
        """,
        (patient_id,),
    ).fetchall()


def get_measurement(measurement_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM measurements WHERE id = ?", (measurement_id,)
    ).fetchone()


def create_measurement(patient_id, param_type, value, unit, recorded_by):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO measurements (patient_id, param_type, value, unit, recorded_by, recorded_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """,
        (patient_id, param_type, value, unit, recorded_by),
    )
    db.commit()
    return cur.lastrowid


def update_measurement(measurement_id, value):
    db = get_db()
    db.execute(
        "UPDATE measurements SET value = ? WHERE id = ?",
        (value, measurement_id),
    )
    db.commit()


# --- Huomiot -------------------------------------------------------------------

def get_notes_for_patient(patient_id):
    db = get_db()
    return db.execute(
        """
        SELECT * FROM notes
        WHERE patient_id = ?
        ORDER BY created_at DESC
        """,
        (patient_id,),
    ).fetchall()


def create_note(patient_id, content, author):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO notes (patient_id, content, author, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """,
        (patient_id, content, author),
    )
    db.commit()
    return cur.lastrowid
