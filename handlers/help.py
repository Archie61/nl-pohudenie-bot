from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

HELP_ARTICLES = {
    "tips": "💪 **Советы по похудению:**

1️⃣ Пейте 2-3 литра воды в день
2️⃣ Ешьте овощи и белки
3️⃣ Занимайтесь спортом 3-4 раза в неделю
4️⃣ Спите 7-8 часов
5️⃣ Избегайте сладкого и фастфуда",
    
    "products": "📦 **Рекомендуемые продукты для похудения:**

✅ Activize Oxyden - энергия и метаболизм
✅ Green Tea - сжигание жира
✅ NutriShake - замена приёма пищи
✅ Aloe Vera - здоровье ЖКТ",
    
    "nutrition": "🥗 **Правильное питание:**

• Завтрак: каша + фрукты
• Обед: белок + овощи + углеводы
• Ужин: лёгкий салат или суп
• Снеки: фрукты, йогурт, орехи",
    
    "sport": "🏃 **Спорт и тренировки:**

• Кардио: 30 минут, 3-4 раза в неделю
• Силовые упражнения: 2 раза в неделю
• Растяжка: ежедневно по 10 минут
• Ходьба: 10 000 шагов в день",
}

@router.callback_query(F.data == "help")
async def help_menu(callback: types.CallbackQuery):
    """Меню помощи"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💪 Советы по похудению", callback_data="help_tips")],
        [InlineKeyboardButton(text="📦 Рекомендуемые продукты", callback_data="help_products")],
        [InlineKeyboardButton(text="🥗 Правильное питание", callback_data="help_nutrition")],
        [InlineKeyboardButton(text="🏃 Спорт и тренировки", callback_data="help_sport")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])
    
    await callback.message.edit_text(
        "💪 **Помощь в похудении**

Выберите интересующий раздел:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("help_"))
async def show_help_article(callback: types.CallbackQuery):
    """Показать статью"""
    article_key = callback.data.split("_", 1)[1]
    
    if article_key not in HELP_ARTICLES:
        await callback.answer("Статья не найдена", show_alert=True)
        return
    
    text = HELP_ARTICLES[article_key]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к помощи", callback_data="help")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()
