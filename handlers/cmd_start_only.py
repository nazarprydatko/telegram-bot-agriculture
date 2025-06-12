from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

async def cmd_start(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Додати посів", callback_data="add_crop"),
                InlineKeyboardButton(text="📄 Подивитися посіви", callback_data="view_crops"),
            ],
            [
                InlineKeyboardButton(text="🗑 Видалити дані", callback_data="delete_data"),
                InlineKeyboardButton(text="🌦 Дізнатися погоду", callback_data="get_weather"),
            ],
            [
                InlineKeyboardButton(text="📊 Розрахувати рентабельність", callback_data="calculate_profit"),
                InlineKeyboardButton(text="📜 Звіт у PDF", callback_data="generate_report"),
            ],
            [
                InlineKeyboardButton(text="📂 Звіт у Excel", callback_data="export_to_excel"),
                InlineKeyboardButton(text="🌱 Додати стан посіву", callback_data="add_condition"),
            ],
            [
                InlineKeyboardButton(text="🌾 Записати врожай", callback_data="record_harvest"),
                InlineKeyboardButton(text="💰 Додати витрати", callback_data="add_expenses"),
            ],
            [
                InlineKeyboardButton(text="✏️ Редагувати посів", callback_data="edit_crop"),
            ]
        ]
    )
    await state.clear()
    await message.answer(
        "🌾 **Вітаємо у Telegram-боті для агрофірми!**\n\n"
        "Оберіть дію за допомогою кнопок нижче:",
        reply_markup=keyboard
    )
