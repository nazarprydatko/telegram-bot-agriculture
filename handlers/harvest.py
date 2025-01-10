from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import execute_query

async def process_harvest_data(message: Message, state: FSMContext):
    try:
        crop_id, harvest_date, workers_count, total_mass = map(str.strip, message.text.split(","))
        crop_id = int(crop_id)
        workers_count = int(workers_count)
        total_mass = float(total_mass)

        if workers_count <= 0:
            raise ValueError("Кількість працівників повинна бути більше 0.")
        if total_mass <= 0:
            raise ValueError("Маса врожаю повинна бути більше 0.")

        execute_query(
            "INSERT INTO harvest (crop_id, harvest_date, workers_count, total_mass) VALUES (%s, %s, %s, %s);",
            (crop_id, harvest_date, workers_count, total_mass)
        )
        await message.reply(f"✅ Врожай успішно додано для посіву {crop_id}!")
    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")
    finally:
        if state:
            await state.clear()
