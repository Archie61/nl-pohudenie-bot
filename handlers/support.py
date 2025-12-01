from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_feedback
from config import MANAGER_ID

router = Router()

class SupportStates(StatesGroup):
    waiting_for_message = State()

@router.callback_query(F.data == "support")
async def support_menu(callback: types.CallbackQuery):
    """Меню поддержки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оставить сообщение", callback_data="support_message")],
        [InlineKeyboardButton(text="❓ FAQ", callback_data="support_faq")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])
    
    await callback.message.edit_text(
        "💬 **Служба поддержки**

Как мы можем вам помочь?",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "support_message")
async def support_message(callback: types.CallbackQuery, state: FSMContext):
    """Форма обратной связи"""
    await callback.message.edit_text("📝 Напишите ваше сообщение (максимум 500 символов):")
    await state.set_state(SupportStates.waiting_for_message)
    await callback.answer()

@router.message(SupportStates.waiting_for_message)
async def process_support_message(message: types.Message, state: FSMContext, bot):
    """Обработка сообщения поддержки"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text
    
    if len(text) > 500:
        await message.answer("❌ Сообщение слишком длинное! Максимум 500 символов.")
        return
    
    # Сохраняем в БД
    add_feedback(user_id, text)
    
    # Отправляем менеджеру
    manager_text = f"""
📨 **Новое сообщение от пользователя**

👤 Имя: {user_name}
🆔 ID: {user_id}
📝 Сообщение: {text}
    """
    
    try:
        await bot.send_message(MANAGER_ID, manager_text, parse_mode="Markdown")
    except:
        pass
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])
    
    await message.answer(
        "✅ Спасибо за сообщение!

Менеджер свяжется с вами в течение 24 часов.",
        reply_markup=keyboard
    )
    await state.clear()

@router.callback_query(F.data == "support_faq")
async def support_faq(callback: types.CallbackQuery):
    """FAQ"""
    text = """
❓ **Часто задаваемые вопросы**

**Q: Какие способы оплаты вы принимаете?**
A: Мы принимаем платёжные системы и переводы.

**Q: Как быстро доставка?**
A: Доставка занимает 3-7 рабочих дней.

**Q: Могу ли я вернуть товар?**
A: Да, в течение 14 дней после покупки.

**Q: Как стать партнёром?**
A: Нажмите "Партнёрская программа" и заполните форму.

**Q: Какие продукты лучше для похудения?**
A: Зависит от вашего типа тела. Напишите нам!
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Задать вопрос", callback_data="support_message")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="support")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()
