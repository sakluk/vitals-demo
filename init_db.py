"""
init_db.py — Luo VitalsDemo-tietokannan (SQLite) ja täyttää sen esimerkkidatalla.

Käyttö:
    python init_db.py

Skripti poistaa mahdollisen vanhan vitals.db-tiedoston ja luo uuden.
"""

import os
import sqlite3
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "vitals.db")

SCHEMA = """
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dob TEXT,
    room TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    param_type TEXT NOT NULL,
    value TEXT NOT NULL,
    unit TEXT,
    recorded_by TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
);
"""

USERS = [
    ("hoitaja", "hoitaja123", "hoitaja"),
    ("laakari", "laakari123", "laakari"),
]

PATIENTS = [
    ("Matti Virtanen", "1955-03-12", "A101"),
    ("Leila Korhonen", "1968-07-24", "A102"),
    ("Pekka Mäkinen", "1942-11-05", "B201"),
    ("Tuula Leinonen", "1975-01-30", "B203"),
    ("Jorma Heikkinen", "1990-09-18", "C301"),
]

# (param_type, value, unit) — 2–4 per potilas, kirjaajana vuorotellen hoitaja/laakari
MEASUREMENT_SETS = [
    [("HR", "72", "bpm"), ("SpO2", "97", "%"), ("TEMP", "36.7", "°C")],
    [("HR", "88", "bpm"), ("NIBP", "128/82", "mmHg")],
    [("RR", "18", "/min"), ("SpO2", "94", "%"), ("HR", "105", "bpm"), ("TEMP", "37.9", "°C")],
    [("HR", "64", "bpm"), ("NIBP", "118/76", "mmHg"), ("SpO2", "99", "%")],
    [("HR", "80", "bpm"), ("RR", "16", "/min")],
]

NOTES = [
    "Potilas vointi vakaa, ei erityishuomioita.",
    "Verenpaine seurannassa, kontrolli huomenna.",
    "Happisaturaatio hieman matala, tarkkaillaan.",
    "Kuume laskussa, jatketaan nykyistä hoitoa.",
    "Potilas liikkeellä avustettuna, hyvä vointi.",
]


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Poistettu vanha tietokanta: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    for username, password, role in USERS:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role),
        )

    recorders = ["hoitaja", "laakari"]
    for i, (name, dob, room) in enumerate(PATIENTS):
        cur = conn.execute(
            "INSERT INTO patients (name, dob, room, created_at) VALUES (?, ?, ?, datetime('now'))",
            (name, dob, room),
        )
        patient_id = cur.lastrowid

        for j, (param_type, value, unit) in enumerate(MEASUREMENT_SETS[i]):
            recorded_by = recorders[j % 2]
            conn.execute(
                """
                INSERT INTO measurements
                    (patient_id, param_type, value, unit, recorded_by, recorded_at)
                VALUES (?, ?, ?, ?, ?, datetime('now', ?))
                """,
                (patient_id, param_type, value, unit, recorded_by, f"-{(len(MEASUREMENT_SETS[i]) - j)} hours"),
            )

        conn.execute(
            """
            INSERT INTO notes (patient_id, content, author, created_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (patient_id, NOTES[i], "laakari"),
        )

    conn.commit()
    conn.close()

    print(f"Tietokanta luotu: {DB_PATH}")
    print(f"  Käyttäjät: {len(USERS)}")
    print(f"  Potilaat: {len(PATIENTS)}")
    print("Kirjautumistunnukset:")
    for username, password, role in USERS:
        print(f"  {username} / {password}  (rooli: {role})")


if __name__ == "__main__":
    main()
