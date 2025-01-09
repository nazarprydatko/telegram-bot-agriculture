from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from handlers.crops import callback_view_crops, process_crop_data
from handlers.delete import confirm_delete, cancel_delete, process_delete_data
from handlers.weather import process_city_weather
from handlers.conditions import process_condition_data
from handlers.harvest import process_harvest_data
from handlers.expenses import process_expense_data
from handlers.reports import cmd_generate_report, cmd_export_to_excel
from handlers.profit import cmd_calculate_profit

# States for input
class CropStates(StatesGroup):
    waiting_for_crop_data = State()

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

async def cmd_start(message: Message):
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
            ]
        ]
    )
    await message.answer(
        "🌾 **Вітаємо у Telegram-боті для агрофірми!**\n\n"
        "Оберіть дію за допомогою кнопок нижче:",
        reply_markup=keyboard
    )

async def callback_add_crop(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("➕ Введіть дані для додавання посіву: Назва культури, Площа, Дата (YYYY-MM-DD), Прогноз дозрівання (днів).")
    await state.set_state(CropStates.waiting_for_crop_data)

async def callback_delete_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🗑 Введіть ID даних, які потрібно видалити.")
    await state.set_state(DeleteStates.waiting_for_delete_id)

async def callback_get_weather(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🌦 Введіть назву міста для отримання погоди:")
    await state.set_state(WeatherStates.waiting_for_city)

async def callback_add_condition(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🌱 Введіть стан посіву: ID, Вологість ґрунту, Температура, Опади.")
    await state.set_state(ConditionStates.waiting_for_condition)

async def callback_record_harvest(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🌾 Введіть дані для врожаю: ID посіву, Дата, Кількість працівників, Маса.")
    await state.set_state(HarvestStates.waiting_for_harvest)

async def callback_add_expenses(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("💰 Введіть дані для витрат: ID посіву, Категорія витрат, Сума.")
    await state.set_state(ExpenseStates.waiting_for_expenses)

async def callback_calculate_profit(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")  # Лог для перевірки
    await cmd_calculate_profit(callback.message)

async def callback_generate_report(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")  # Лог для перевірки
    await cmd_generate_report(callback.message)

async def callback_export_to_excel(callback: CallbackQuery):
    print(f"Callback received: {callback.data}")  # Лог для перевірки
    await cmd_export_to_excel(callback.message)

def register_callbacks(dp: Dispatcher):
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
    dp.callback_query.register(confirm_delete, lambda c: c.data == "confirm_delete")
    dp.callback_query.register(cancel_delete, lambda c: c.data == "cancel_delete")
