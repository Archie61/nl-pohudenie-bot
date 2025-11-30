import sqlite3
from datetime import datetime
import os

DB_FILE = "leads.db"

def init_db():
    """Создать базу данных если её нет"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            name TEXT,
            age INTEGER,
            current_weight REAL,
            goal TEXT,
            problem TEXT,
            username TEXT,
            registered_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def save_lead(user_id, name, age, weight, goal, problem, username):
    """Сохранить лид в БД"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO leads (user_id, name, age, current_weight, goal, problem, username, registered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, age, weight, goal, problem, username, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
        conn.close()
        print(f"✅ Лид сохранен: {name}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        return False

def get_lead(user_id):
    """Получить данные лида"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM leads WHERE user_id = ?', (user_id,))
        lead = cursor.fetchone()
        conn.close()
        return lead
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return None

def get_stats():
    """Получить статистику"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM leads')
        total = cursor.fetchone()[0]
        conn.close()
        return {"total": total}
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")
        return {"total": 0}
