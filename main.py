import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, MANAGER_ID
from database import init_db

# Импортируем все handlers
from handlers import start, auth, catalog, partner, help as help_handler, support

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    """Главная функция"""
    # Инициализируем БД
    init_db()
    
    # Регистрируем все роутеры
    dp.include_router(start.router)
    dp.include_router(auth.router)
    dp.include_router(catalog.router)
    dp.include_router(partner.router)
    dp.include_router(help_handler.router)
    dp.include_router(support.router)
    
    # Удаляем старый вебхук и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ База данных инициализирована")
    print("🚀 Бот запущен!")
    
    # Запускаем поллинг
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
