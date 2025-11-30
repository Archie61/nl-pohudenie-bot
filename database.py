import sqlite3
from datetime import datetime

DB_FILE = "leads.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        name TEXT,
        age INTEGER,
        weight REAL,
        goal TEXT,
        problem TEXT,
        username TEXT,
        date TEXT
    )''')
    conn.commit()
    conn.close()

def save_lead(user_id, name, age, weight, goal, problem, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO leads VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (user_id, name, age, weight, goal, problem, username, 
                   datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
    except:
        pass
    conn.close()
