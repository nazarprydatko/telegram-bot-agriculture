from aiogram.types import Message
from database import execute_query

async def cmd_add_condition(message: Message):
    await message.reply("Введіть: ID посіву, Вологість ґрунту (%), Температура (°C), Опади (мм).")

async def process_condition_data(message: Message):
    try:
        crop_id, soil_moisture, temperature, precipitation = map(str.strip, message.text.split(","))
        execute_query(
            "INSERT INTO crop_conditions (crop_id, soil_moisture, temperature, precipitation) VALUES (%s, %s, %s, %s)",
            (int(crop_id), float(soil_moisture), float(temperature), float(precipitation))
        )
        await message.reply(f"✅ Дані стану для посіву ID {crop_id} успішно додано!")
    except Exception as e:
        await message.reply(f"❌ Помилка: {e}")
