import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from config import BOT_TOKEN, MANAGER_ID
from database import init_db, save_lead

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    name = State()
    age = State()
    weight = State()
    goal = State()
    problem = State()

init_db()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📝 Анкета", callback_data="reg")],
        [types.InlineKeyboardButton(text="💊 Продукты", callback_data="prod")],
    ])
    await message.answer("👋 Похудение с NL!\n\nЗаполните анкету:", reply_markup=kb)

@dp.callback_query(F.data == "reg")
async def register(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Ваше имя:")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Возраст:")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Вес (кг):")
    await state.set_state(Form.weight)

@dp.message(Form.weight)
async def get_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=float(message.text))
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Похудеть", callback_data="lose")],
        [types.InlineKeyboardButton(text="Набрать", callback_data="gain")],
    ])
    await message.answer("Цель:", reply_markup=kb)
    await state.set_state(Form.goal)

@dp.callback_query(Form.goal)
async def get_goal(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(goal=query.data)
    await query.message.edit_text("Проблема:")
    await state.set_state(Form.problem)

@dp.message(Form.problem)
async def get_problem(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    save_lead(message.from_user.id, data['name'], data['age'], 
              data['weight'], data['goal'], message.text, 
              message.from_user.username or "нет")
    
    text = f"🆕 Новый клиент!\n👤 {data['name']}\n⚖️ {data['weight']} кг"
    await bot.send_message(MANAGER_ID, text)
    
    await message.answer("✅ Данные сохранены!")
    await state.clear()

@dp.callback_query(F.data == "prod")
async def products(query: types.CallbackQuery):
    await query.message.edit_text("💊 Energy Diet, Smart GO, Greenflash")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
