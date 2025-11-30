from aiogram import Router, F, types, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_user, get_user, update_user_contact

router = Router()

class AuthStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_email = State()

@router.callback_query(F.data == "profile")
async def profile_menu(callback: types.CallbackQuery):
    """Меню профиля"""
    user_id = callback.from_user.id
    user = get_user(user_id)
    
    # Если пользователя нет в БД - регистрируем
    if not user:
        add_user(user_id, callback.from_user.username, callback.from_user.first_name)
        user = get_user(user_id)
    
    phone = user[3] if user[3] else "Не указан"
    email = user[4] if user[4] else "Не указан"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Изменить телефон", callback_data="edit_phone")],
        [InlineKeyboardButton(text="📧 Изменить email", callback_data="edit_email")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])
    
    text = f"""
👤 **Ваш профиль**

Имя: {user[2]}
Телефон: {phone}
Email: {email}
Статус: {'🤝 Партнёр' if user[5] else '👤 Пользователь'}
    """
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "edit_phone")
async def edit_phone(callback: types.CallbackQuery, state: FSMContext):
    """Редактирование телефона"""
    await callback.message.edit_text("📱 Введите ваш номер телефона:")
    await state.set_state(AuthStates.waiting_for_phone)
    await callback.answer()

@router.message(AuthStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    """Обработка телефона"""
    phone = message.text
    user_id = message.from_user.id
    
    user = get_user(user_id)
    email = user[4] if user[4] else ""
    
    update_user_contact(user_id, phone, email)
    
    await message.answer("✅ Телефон сохранён!")
    await state.clear()
    
    # Вернуться в профиль
    await callback_to_profile(message, user_id)

@router.callback_query(F.data == "edit_email")
async def edit_email(callback: types.CallbackQuery, state: FSMContext):
    """Редактирование email"""
    await callback.message.edit_text("📧 Введите ваш email:")
    await state.set_state(AuthStates.waiting_for_email)
    await callback.answer()

@router.message(AuthStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    """Обработка email"""
    email = message.text
    user_id = message.from_user.id
    
    user = get_user(user_id)
    phone = user[3] if user[3] else ""
    
    update_user_contact(user_id, phone, email)
    
    await message.answer("✅ Email сохранён!")
    await state.clear()

async def callback_to_profile(message: types.Message, user_id: int):
    """Вспомогательная функция для возврата в профиль"""
    pass
