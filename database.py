from dotenv import load_dotenv
import os 
import sqlite3
from werkzeug.security import generate_password_hash
import json


load_dotenv()
database_path = os.getenv("DB_PATH")

def get_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS exercise (
                id                TEXT PRIMARY KEY,
                name              TEXT NOT NULL,
                category          TEXT,
                body_part         TEXT,
                equipment         TEXT,
                instructions      TEXT,
                muscle_group      TEXT,
                secondary_muscles TEXT,
                target            TEXT,
                image             TEXT,
                gif_url           TEXT,
                created_at        TIMESTAMP
            );
        """)

        conn.commit()
    
    seed_db()

def seed_db():
    seed_users()
    seed_exercises()

def seed_users():
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users;").fetchone()[0]

        if count > 0:
            return
        
        users = [
            (os.getenv("ADMIN_USERNAME"), generate_password_hash(os.getenv("ADMIN_PASSWORD")))
        ]

        conn.executemany("""
            INSERT INTO users (login, password) 
            VALUES (?, ?);
        """, users)

        conn.commit()

def seed_exercises():
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM exercise;").fetchone()[0]

        if count > 0:
            return

        data_path = os.getenv("DATA_PATH")
        if not data_path:
            raise ValueError("DATA_PATH env not set")

        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        processed_data = []

        for item in raw_data:
            secondary_muscles = item.get("secondary_muscles")

            if isinstance(secondary_muscles, list):
                secondary_muscles = ", ".join(secondary_muscles)

            instructions = item.get("instructions", {}).get("en")

            exercise_tuple = (
                item.get("id"),
                item.get("name"),
                item.get("category"),
                item.get("body_part"),
                item.get("equipment"),
                instructions,
                item.get("muscle_group"),
                secondary_muscles,
                item.get("target"),
                item.get("image"),
                item.get("gif_url"),
                item.get("created_at"),
            )
            processed_data.append(exercise_tuple)

        conn.executemany("""
            INSERT OR REPLACE INTO exercise (
                id, name, category, body_part, equipment, instructions,
                muscle_group, secondary_muscles, target, image, gif_url, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, processed_data,)

        conn.commit()


# -------------------------
# LOGIN HELPER FUNCTIONS 
# ------------------------

def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE login = ?;",(username,)).fetchone()
        return dict(row) if row else None

# ---------------------------
# EXERCISE HELPER FUNCTIONS
# ---------------------------

def get_all_exercises():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM exercise ORDER BY id")
        return [dict(row) for row in rows]