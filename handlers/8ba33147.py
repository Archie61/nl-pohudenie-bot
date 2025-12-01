from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import register_as_partner, get_user

router = Router()


class PartnerStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


@router.callback_query(F.data == "partner")
async def partner_menu(callback: types.CallbackQuery):
    """Меню партнёрской программы"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 О программе", callback_data="partner_info")],
        [InlineKeyboardButton(text="📝 Стать партнёром", callback_data="partner_register")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])

    await callback.message.edit_text(
        "🤝 **Партнёрская программа NL International**",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

    await callback.answer()


@router.callback_query(F.data == "partner_info")
async def partner_info(callback: types.CallbackQuery):
    """Информация о программе"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Стать партнёром", callback_data="partner_register")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="partner")],
    ])

    text = """🤝 **Условия партнёрской программы:**

✅ **Комиссия:** 15-30% от каждой продажи
✅ **Бонусы:** Дополнительные премии за объём продаж
✅ **Поддержка:** Личный менеджер для каждого партнёра
✅ **Материалы:** Готовые презентации и каталоги
✅ **Обучение:** Бесплатные вебинары и тренинги

💰 **Зарплата партнёров:**
- До 5 продаж/месяц: 15%
- 5-15 продаж/месяц: 20%
- 15+ продаж/месяц: 25-30%

🎁 **Бонусы:**
- За первых 10 клиентов: 50$
- За 50 клиентов: 500$
- За 100+ клиентов: премия в путешествие!

📞 Менеджер: +1-800-NL-INTL"""

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

    await callback.answer()


@router.callback_query(F.data == "partner_register")
async def partner_register(callback: types.CallbackQuery, state: FSMContext):
    """Регистрация партнёра"""
    user_id = callback.from_user.id
    user = get_user(user_id)

    if user and user[5]:  # Уже партнёр
        await callback.answer("Вы уже зарегистрированы как партнёр!", show_alert=True)
        return

    await callback.message.edit_text(
        "📝 Давайте начнём регистрацию!\n\nВведите ваше полное имя:"
    )

    await state.set_state(PartnerStates.waiting_for_name)

    await callback.answer()


@router.message(PartnerStates.waiting_for_name)
async def process_partner_name(message: types.Message, state: FSMContext):
    """Обработка имени партнёра"""
    await state.update_data(name=message.text)

    await message.answer("Теперь введите ваш номер телефона:")

    await state.set_state(PartnerStates.waiting_for_phone)


@router.message(PartnerStates.waiting_for_phone)
async def process_partner_phone(message: types.Message, state: FSMContext):
    """Обработка телефона партнёра"""
    data = await state.get_data()
    name = data.get("name")
    phone = message.text
    user_id = message.from_user.id

    # Регистрируем как партнёра
    register_as_partner(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])

    text = f"""✅ **Поздравляем!**

Вы успешно зарегистрировались как партнёр NL International! 🎉

👤 Имя: {name}
📱 Телефон: {phone}
🔗 Ваша реферальная ссылка: https://t.me/nl_pohudenie_bot?start=ref_{user_id}

Пригласите друзей по этой ссылке и получайте комиссию!

📞 Менеджер свяжется с вами в течение 24 часов."""

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

    await state.clear()
