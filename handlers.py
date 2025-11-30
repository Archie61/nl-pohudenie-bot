from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from config import MANAGER_ID
from database import save_lead

router = Router()

class Form(StatesGroup):
    name = State()
    age = State()
    weight = State()
    goal = State()
    problem = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Заполнить анкету", callback_data="register")],
        [InlineKeyboardButton(text="💊 Продукты NL", callback_data="products")],
        [InlineKeyboardButton(text="📞 Консультант", callback_data="contact")]
    ])
    await message.answer(
        "👋 **Хотите избавиться от лишнего веса?**\n\n"
        "✅ *Программы похудения NL International*\n"
        "✅ *Коктейли Energy Diet* и *Smart GO*\n"
        "✅ *БАДы Greenflash* для метаболизма\n\n"
        "**Заполните анкету за 1 минуту!**",
        reply_markup=kb, parse_mode="Markdown"
    )

@router.callback_query(F.data == "register")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📝 **Введите ваше имя:**")
    await state.set_state(Form.name)
    await callback.answer()

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("🎂 **Ваш возраст:**")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16 or int(message.text) > 100:
        return await message.answer("⚠️ **Введите возраст числом (16-100):**")
    await state.update_data(age=int(message.text))
    await message.answer("⚖️ **Текущий вес (кг):**")
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 30 or weight > 300:
            raise ValueError
        await state.update_data(current_weight=weight)
    except ValueError:
        return await message.answer("⚠️ **Вес числом (30-300 кг), например: 85.5**")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➖ Похудеть", callback_data="goal_lose")],
        [InlineKeyboardButton(text="➕ Набрать", callback_data="goal_gain")],
        [InlineKeyboardButton(text="➖/➕ Поддерживать", callback_data="goal_hold")]
    ])
    await message.answer("🎯 **Какая ваша цель?**", reply_markup=kb)
    await state.set_state(Form.goal)

@router.callback_query(Form.goal)
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goals = {
        "goal_lose": "Похудеть", 
        "goal_gain": "Набрать", 
        "goal_hold": "Поддерживать"
    }
    await state.update_data(goal=goals[callback.data])
    await callback.message.edit_text(
        "😟 **Какая основная проблема?**\n"
        "_переедание, гормоны, медленный метаболизм, отеки, другое_",
        parse_mode="Markdown"
    )
    await state.set_state(Form.problem)
    await callback.answer()

@router.message(Form.problem)
async def process_problem(message: Message, state: FSMContext):
    data = await state.get_data()
    username = message.from_user.username or "нет"
    
    # Сохраняем в Google Sheets
    await save_lead(
        message.from_user.id, data['name'], data['age'], 
        data['current_weight'], data['goal'], message.text, username
    )
    
    # Уведомление жене
    lead_text = (
        f"🆕 **Новый клиент!**\n\n"
        f"👤 {data['name']}, {data['age']} лет\n"
        f"⚖️ {data['current_weight']} кг\n"
        f"🎯 {data['goal']}\n"
        f"😟 {message.text}\n\n"
        f"🆔 @{username} (ID: {message.from_user.id})"
    )
    await message.bot.send_message(MANAGER_ID, lead_text, parse_mode="Markdown")
    
    # Подтверждение
    await message.answer(
        "✅ **Спасибо! Данные приняты.**\n\n"
        "💌 *Диетолог свяжется в течение 30 минут*\n"
        "для подбора **индивидуальной программы NL**!\n\n"
        "⏰ Обычно отвечает быстро.",
        parse_mode="Markdown"
    )
    await state.clear()
