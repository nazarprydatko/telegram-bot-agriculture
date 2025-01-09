import asyncio
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from handlers.start import (
    cmd_start,
    register_callbacks,
    CropStates, DeleteStates, WeatherStates, ConditionStates, HarvestStates, ExpenseStates
)
from handlers.crops import process_crop_data
from handlers.delete import process_delete_data
from handlers.weather import process_city_weather
from handlers.conditions import process_condition_data
from handlers.harvest import process_harvest_data
from handlers.expenses import process_expense_data
from utils.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.message.register(cmd_start, Command("start"))
dp.message.register(process_crop_data, CropStates.waiting_for_crop_data)
dp.message.register(process_delete_data, DeleteStates.waiting_for_delete_id)
dp.message.register(process_city_weather, WeatherStates.waiting_for_city)
dp.message.register(process_condition_data, ConditionStates.waiting_for_condition)
dp.message.register(process_harvest_data, HarvestStates.waiting_for_harvest)
dp.message.register(process_expense_data, ExpenseStates.waiting_for_expenses)

register_callbacks(dp)

async def main():
    print("Бот запущено...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
