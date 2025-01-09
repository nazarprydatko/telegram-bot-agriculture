from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database import fetch_all, execute_query


async def cmd_add_crop(message: Message, state: FSMContext):
    await message.reply(
        "Введіть дані для посіву: Назва культури, Площа (га), Дата посіву (YYYY-MM-DD), Прогноз дозрівання (днів)."
    )
    await state.set_state("waiting_for_crop_data")

async def process_crop_data(message: Message, state: FSMContext):
    try:
        data = message.text.split(",")
        if len(data) != 4:
            raise ValueError("Некоректний формат. Введіть: Назва культури, Площа, Дата, Прогноз.")

        name, area, sowing_date, maturation_days = map(str.strip, data)

        area = float(area)
        maturation_days = int(maturation_days)
        from datetime import datetime
        datetime.strptime(sowing_date, "%Y-%m-%d")

        print(f"Adding crop: {name}, {area}, {sowing_date}, {maturation_days}")

        query = """
        INSERT INTO crops (name, area, sowing_date, maturation_days)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (name, area, sowing_date, maturation_days))
        await message.reply(f"✅ Дані для посіву '{name}' успішно додано!")
    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")
    finally:
        await state.clear()

async def callback_view_crops(callback: CallbackQuery):
    try:
        query = "SELECT id, name, area, sowing_date FROM crops;"
        crops = fetch_all(query)

        if not crops:
            await callback.message.answer("❌ Посівів ще немає.")
            return

        response = "🌾 **Список посівів:**\n"
        for crop in crops:
            response += f"ID: {crop[0]}, Назва: {crop[1]}, Площа: {crop[2]} га, Дата посіву: {crop[3]}\n"

        await callback.message.answer(response)
    except Exception as e:
        await callback.message.answer(f"❌ Сталася помилка: {e}")