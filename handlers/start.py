from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

async def get_main_menu():
    """Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="💪 Помощь в похудении", callback_data="help")],
        [InlineKeyboardButton(text="🤝 Партнёрская программа", callback_data="partner")],
        [InlineKeyboardButton(text="💬 Поддержка", callback_data="support")],
    ])
    return keyboard

@router.message(CommandStart())
async def start_handler(message: types.Message):
    """Команда /start"""
    keyboard = await get_main_menu()
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!

"
        "Добро пожаловать в NL International бот для похудения! 💪

"
        "Выберите, что вас интересует:",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Вернуться в главное меню"""
    keyboard = await get_main_menu()
    await callback.message.edit_text(
        "📌 Главное меню",
        reply_markup=keyboard
    )
    await callback.answer()
