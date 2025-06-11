from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram import Dispatcher, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from handlers.crops import confirm_crop, cancel_crop
from handlers.harvest import confirm_harvest, cancel_harvest
from handlers.expenses import confirm_expense, cancel_expense
from handlers.conditions import confirm_condition, cancel_condition

from handlers.crops import callback_view_crops
from handlers.delete import confirm_delete, cancel_delete
from handlers.reports import cmd_generate_report, cmd_export_to_excel
from handlers.profit import cmd_calculate_profit
from handlers.edit_crop import callback_edit_crop, process_edit_crop_id, process_edit_crop_data

# Клавіатура "Головне меню"
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏠 Головне меню")]],
    resize_keyboard=True,
    one_time_keyboard=False
)

class CropStates(StatesGroup):
    waiting_for_crop_data = State()
    edit_crop_id = State()
    edit_crop_data = State()

class DeleteStates(StatesGroup):
    waiting_for_delete_id = State()

class WeatherStates(StatesGroup):
    waiting_for_city = State()

class ConditionStates(StatesGroup):
    waiting_for_condition = State()

class HarvestStates(StatesGroup):
    waiting_for_harvest = State()

class ExpenseStates(StatesGroup):
    waiting_for_expenses = State()

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


async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()  # Очищаємо стан FSM
    await cmd_start(message, state)


# Callback  з кнопкою повернення
async def callback_add_crop(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "➕ Введіть дані для додавання посіву: Назва культури, Площа, Дата (YYYY-MM-DD), Прогноз дозрівання (днів).",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(CropStates.waiting_for_crop_data)

async def callback_delete_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🗑 Введіть ID даних, які потрібно видалити.",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(DeleteStates.waiting_for_delete_id)

async def callback_get_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🌦 Введіть назву міста для отримання погоди:",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(WeatherStates.waiting_for_city)

async def callback_add_condition(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🌱 Введіть стан посіву: ID, Вологість ґрунту, Температура, Опади.",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(ConditionStates.waiting_for_condition)

async def callback_record_harvest(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🌾 Введіть дані для врожаю: ID посіву, Дата, Кількість працівників, Маса.",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(HarvestStates.waiting_for_harvest)

async def callback_add_expenses(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "💰 Введіть дані для витрат: ID посіву, Категорія витрат, Сума.",
        reply_markup=main_menu_keyboard
    )
    await state.set_state(ExpenseStates.waiting_for_expenses)

async def callback_calculate_profit(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")
    await cmd_calculate_profit(callback.message)

async def callback_generate_report(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")
    await cmd_generate_report(callback.message)

async def callback_export_to_excel(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")
    await cmd_export_to_excel(callback.message)

# Реєстрація callback
def register_callbacks(dp: Dispatcher):
    dp.message.register(back_to_main_menu, F.text == "🏠 Головне меню")

    dp.callback_query.register(callback_add_crop, lambda c: c.data == "add_crop")
    dp.callback_query.register(callback_view_crops, lambda c: c.data == "view_crops")
    dp.callback_query.register(callback_delete_data, lambda c: c.data == "delete_data")
    dp.callback_query.register(callback_get_weather, lambda c: c.data == "get_weather")
    dp.callback_query.register(callback_calculate_profit, lambda c: c.data == "calculate_profit")
    dp.callback_query.register(callback_generate_report, lambda c: c.data == "generate_report")
    dp.callback_query.register(callback_export_to_excel, lambda c: c.data == "export_to_excel")
    dp.callback_query.register(callback_add_condition, lambda c: c.data == "add_condition")
    dp.callback_query.register(callback_record_harvest, lambda c: c.data == "record_harvest")
    dp.callback_query.register(callback_add_expenses, lambda c: c.data == "add_expenses")
    dp.callback_query.register(callback_edit_crop, lambda c: c.data == "edit_crop")
    dp.message.register(process_edit_crop_id, CropStates.edit_crop_id)
    dp.message.register(process_edit_crop_data, CropStates.edit_crop_data)
    dp.callback_query.register(confirm_delete, lambda c: c.data == "confirm_delete")
    dp.callback_query.register(cancel_delete, lambda c: c.data == "cancel_delete")
    dp.callback_query.register(confirm_crop, lambda c: c.data == "confirm_crop")
    dp.callback_query.register(cancel_crop, lambda c: c.data == "cancel_crop")
    dp.callback_query.register(confirm_harvest, lambda c: c.data == "confirm_harvest")
    dp.callback_query.register(cancel_harvest, lambda c: c.data == "cancel_harvest")
    dp.callback_query.register(confirm_expense, lambda c: c.data == "confirm_expense")
    dp.callback_query.register(cancel_expense, lambda c: c.data == "cancel_expense")
    dp.callback_query.register(confirm_condition, lambda c: c.data == "confirm_condition")
    dp.callback_query.register(cancel_condition, lambda c: c.data == "cancel_condition")
