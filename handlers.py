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
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Anketa", callback_data="register")],
        [InlineKeyboardButton(text="Products", callback_data="products")],
        [InlineKeyboardButton(text="Contact", callback_data="contact")]
    ])
    await message.answer(
        "Welcome to NL diet program!",
        reply_markup=kb
    )

@router.callback_query(F.data == "register")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Your name:")
    await state.set_state(Form.name)
    await callback.answer()

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Your age:")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 16 or age > 100:
            return await message.answer("Age 16-100 please:")
        await state.update_data(age=age)
        await message.answer("Current weight (kg):")
        await state.set_state(Form.weight)
    except:
        await message.answer("Enter age as number:")

@router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight < 30 or weight > 300:
            raise ValueError
        await state.update_data(current_weight=weight)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Lose weight", callback_data="lose")],
            [InlineKeyboardButton(text="Gain", callback_data="gain")],
        ])
        await message.answer("Your goal:", reply_markup=kb)
        await state.set_state(Form.goal)
    except ValueError:
        await message.answer("Enter weight (30-300 kg):")

@router.callback_query(Form.goal)
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goal_text = "Lose weight" if callback.data == "lose" else "Gain"
    await state.update_data(goal=goal_text)
    await callback.message.edit_text("Main problem:")
    await state.set_state(Form.problem)
    await callback.answer()

@router.message(Form.problem)
async def process_problem(message: Message, state: FSMContext):
    data = await state.get_data()
    username = message.from_user.username or "no"
    
    save_lead(
        message.from_user.id, data['name'], data['age'],
        data['current_weight'], data['goal'], message.text, username
    )
    
    lead_text = (
        f"New client!
"
        f"Name: {data['name']}, {data['age']} years
"
        f"Weight: {data['current_weight']} kg
"
        f"Goal: {data['goal']}
"
        f"Problem: {message.text}
"
        f"User: @{username}"
    )
    await message.bot.send_message(MANAGER_ID, lead_text)
    
    await message.answer("Thank you! We will contact you soon!")
    await state.clear()

@router.callback_query(F.data == "products")
async def products_info(callback: CallbackQuery):
    text = "Energy Diet, Smart GO, Greenflash - best products!"
    await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data == "contact")
async def contact(callback: CallbackQuery):
    await callback.message.edit_text("We will contact you!")
    await callback.answer()
