import pygsheets
import asyncio
from datetime import datetime

gc = None
sheet = None

async def init_sheets():
    global gc, sheet
    gc = pygsheets.authorize(service_file='credentials.json')
    sheet = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sheet.sheet1
    if worksheet.row_count == 0:
        worksheet.update('A1:H1', [['ID', 'Имя', 'Возраст', 'Вес', 'Цель', 'Проблема', 'Дата', 'Telegram']])
    print("✅ Google Sheets подключен")

async def save_lead(user_id, name, age, weight, goal, problem, username):
    global gc, sheet
    if not gc or not sheet:
        print("❌ Sheets не инициализирован")
        return
    
    worksheet = sheet.sheet1
    row = [
        user_id, name, age, weight, goal, problem, 
        datetime.now().strftime('%Y-%m-%d %H:%M'), f"@{username}"
    ]
    worksheet.append_table([row])
    print(f"✅ Лид сохранен: {name}")
