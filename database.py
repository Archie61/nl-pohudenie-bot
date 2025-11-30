import sqlite3
import os
from datetime import datetime

DB_PATH = "bot_database.db"

def init_db():
    """Инициализация БД"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            phone TEXT,
            email TEXT,
            is_registered INTEGER DEFAULT 0,
            is_partner INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица обратной связи
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    """Добавить пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, is_registered)
        VALUES (?, ?, ?, 1)
    ''', (user_id, username, first_name))
    conn.commit()
    conn.close()

def update_user_contact(user_id, phone, email):
    """Обновить контакты"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET phone = ?, email = ? WHERE user_id = ?
    ''', (phone, email, user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получить данные пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def register_as_partner(user_id):
    """Зарегистрировать как партнёра"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET is_partner = 1 WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def add_feedback(user_id, message):
    """Сохранить обратную связь"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    conn.commit()
    conn.close()

def get_all_feedback():
    """Получить всю обратную связь (для менеджера)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedback = cursor.fetchall()
    conn.close()
    return feedback
