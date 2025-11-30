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
        [InlineKeyboardButton(text="Form", callback_data="register")],
        [InlineKeyboardButton(text="Products", callback_data="products")],
    ])
    await message.answer("Welcome! Fill the form:", reply_markup=kb)

@router.callback_query(F.data == "register")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Your name:")
    await state.set_state(Form.name)
    await callback.answer()

@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Your age:")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Weight (kg):")
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=float(message.text))
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Lose", callback_data="lose")],
        [InlineKeyboardButton(text="Gain", callback_data="gain")],
    ])
    await message.answer("Goal:", reply_markup=kb)
    await state.set_state(Form.goal)

@router.callback_query(Form.goal)
async def process_goal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(goal=callback.data)
    await callback.message.edit_text("Problem:")
    await state.set_state(Form.problem)
    await callback.answer()

@router.message(Form.problem)
async def process_problem(message: Message, state: FSMContext):
    data = await state.get_data()
    save_lead(message.from_user.id, data['name'], data['age'], data['weight'], data['goal'], message.text, message.from_user.username or "no")
    text = f"New: {data['name']}, {data['weight']}kg, goal={data['goal']}"
    await message.bot.send_message(MANAGER_ID, text)
    await message.answer("Thanks!")
    await state.clear()

@router.callback_query(F.data == "products")
async def products(callback: CallbackQuery):
    await callback.message.edit_text("Products: Energy Diet, Smart GO")
    await callback.answer()
