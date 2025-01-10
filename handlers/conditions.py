from aiogram.types import Message
from database import execute_query

async def cmd_add_condition(message: Message):
    await message.reply("Введіть: ID посіву, Вологість ґрунту (%), Температура (°C), Опади (мм).")

async def process_condition_data(message: Message):
    try:
        data = message.text.split(",")
        if len(data) != 4:
            raise ValueError("Некоректний формат. Введіть: ID посіву, Вологість ґрунту, Температура, Опади.")

        crop_id, soil_moisture, temperature, precipitation = map(str.strip, data)

        crop_id = int(crop_id)
        soil_moisture = float(soil_moisture)
        temperature = float(temperature)
        precipitation = float(precipitation)

        if soil_moisture < 0 or soil_moisture > 100:
            raise ValueError("Вологість повинна бути в межах 0-100%.")
        if precipitation < 0:
            raise ValueError("Опади не можуть бути від’ємними.")
        if temperature < -100 or temperature > 100:
            raise ValueError("Температура має бути в діапазоні -100°C до 100°C.")

        execute_query(
            "INSERT INTO crop_conditions (crop_id, soil_moisture, temperature, precipitation) VALUES (%s, %s, %s, %s)",
            (crop_id, soil_moisture, temperature, precipitation)
        )
        await message.reply(f"✅ Дані стану для посіву ID {crop_id} успішно додано!")
    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Помилка: {e}")
