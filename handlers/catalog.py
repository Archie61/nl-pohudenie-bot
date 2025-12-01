from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

# Жёсткий список популярных продуктов NL International
PRODUCTS = {
    "weight_loss": [
        {"id": 1, "name": "Activize Oxyden (Активайз Оксиджен)", "price": "25$", "desc": "Напиток для энергии и выносливости"},
        {"id": 2, "name": "Aloe Vera (Алоэ Вера)", "price": "28$", "desc": "Гель Алоэ для здоровья ЖКТ"},
        {"id": 3, "name": "Nutrient Drink Mix (NutriShake)", "price": "35$", "desc": "Коктейль для похудения и здоровья"},
        {"id": 4, "name": "TeaVana Green Tea", "price": "18$", "desc": "Зелёный чай для метаболизма"},
    ],
    "nutrition": [
        {"id": 5, "name": "Omega 3 Plus", "price": "32$", "desc": "Омега-3 для сердца и мозга"},
        {"id": 6, "name": "Multivitamin Formula", "price": "38$", "desc": "Комплекс витаминов и минералов"},
        {"id": 7, "name": "Magnesium Plus", "price": "22$", "desc": "Магний для расслабления и сна"},
    ],
    "skincare": [
        {"id": 8, "name": "NL Face Cream", "price": "42$", "desc": "Крем для лица премиум качества"},
        {"id": 9, "name": "Body Lotion", "price": "24$", "desc": "Лосьон для тела с увлажнением"},
    ],
}

@router.callback_query(F.data == "catalog")
async def catalog_menu(callback: types.CallbackQuery):
    """Меню каталога"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💪 Для похудения", callback_data="cat_weight_loss")],
        [InlineKeyboardButton(text="🥗 Питание и витамины", callback_data="cat_nutrition")],
        [InlineKeyboardButton(text="💄 Уход за кожей", callback_data="cat_skincare")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])
    
    await callback.message.edit_text(
        "📦 **Выберите категорию:**",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("cat_"))
async def show_category(callback: types.CallbackQuery):
    """Показать товары по категории"""
    category = callback.data.split("_", 1)[1]
    
    if category not in PRODUCTS:
        await callback.answer("Категория не найдена", show_alert=True)
        return
    
    products = PRODUCTS[category]
    text = "🏪 Товары в категории:

Выберите интересующую вас категорию:"
    
    for product in products:
        text += f"▪️ {product['name']}
💰 {product['price']}
📝 {product['desc']}

"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="catalog")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()
