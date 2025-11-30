import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_ID = 123456789  # ← ЗАМЕНИТЕ на Telegram ID жены
GOOGLE_SHEET_ID = "1ABC123xyz"  # ← ЗАМЕНИТЕ на ID вашей таблицы
