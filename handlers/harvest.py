from aiogram.types import Message
from database import execute_query

async def cmd_record_harvest(message: Message):
    await message.reply("Введіть: ID посіву, Дата збору (YYYY-MM-DD), Кількість працівників, Маса врожаю (тонн).")

async def process_harvest_data(message: Message):
    try:
        crop_id, harvest_date, workers_count, total_mass = map(str.strip, message.text.split(","))
        execute_query(
            "INSERT INTO harvest (crop_id, harvest_date, workers_count, total_mass) VALUES (%s, %s, %s, %s)",
            (int(crop_id), harvest_date, int(workers_count), float(total_mass))
        )
        await message.reply(f"✅ Дані про врожай для посіву ID {crop_id} успішно додано!")
    except Exception as e:
        await message.reply(f"❌ Помилка: {e}")
