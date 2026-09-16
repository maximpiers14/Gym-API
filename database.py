from dotenv import load_dotenv
import os 
import sqlite3
from werkzeug.security import generate_password_hash


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
            # add all other tables here

        conn.commit()
    
    seed_db()

def seed_db():
    seed_users()

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

# -------------------------------------------
# ALL HELPER FUNCTIONS RELATED TO DATABASE  
# -------------------------------------------

def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE login = ?;",(username,)).fetchone()
        return dict(row) if row else None