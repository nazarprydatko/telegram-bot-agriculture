from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import execute_query
from handlers.start import cmd_start


async def cmd_add_condition(message: Message, state: FSMContext):
    await message.reply("Введіть: ID посіву, Вологість ґрунту (%), Температура (°C), Опади (мм).")
    await state.set_state("waiting_for_condition")


async def process_condition_data(message: Message, state: FSMContext):
    if message.text.strip() == "🏠 Головне меню":
        await state.clear()
        await cmd_start(message, state)
        return

    try:
        data = message.text.split(",")
        if len(data) != 4:
            await message.reply("❌ Формат: ID, Вологість, Температура, Опади")
            return

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

        await state.update_data(
            crop_id=crop_id,
            soil_moisture=soil_moisture,
            temperature=temperature,
            precipitation=precipitation
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Так", callback_data="confirm_condition"),
                InlineKeyboardButton(text="❌ Ні", callback_data="cancel_condition")
            ]
        ])

        await message.reply(
            f"🌱 Ви ввели наступне:\n"
            f"ID посіву: {crop_id}\n"
            f"Вологість ґрунту: {soil_moisture}%\n"
            f"Температура: {temperature}°C\n"
            f"Опади: {precipitation} мм\n\nПідтвердити збереження?",
            reply_markup=keyboard
        )
        await state.set_state("waiting_for_condition_confirmation")

    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except TypeError as te:
        await message.reply(f"❌ Неправильний тип даних: {te}")
    except KeyError as ke:
        await message.reply(f"❌ Відсутній ключ у даних: {ke}")
    except Exception as e:
        await message.reply(f"❌ Неочікувана помилка: {e}")


async def confirm_condition(callback: CallbackQuery, state: FSMContext):
    """Підтверджує збереження стану посіву у базу даних."""
    data = await state.get_data()
    try:
        execute_query(
            "INSERT INTO crop_conditions (crop_id, soil_moisture, temperature, precipitation) VALUES (%s, %s, %s, %s)",
            (data['crop_id'], data['soil_moisture'], data['temperature'], data['precipitation'])
        )
        await callback.message.edit_text("✅ Дані стану успішно додано!")
    except KeyError as ke:
        await callback.message.edit_text(f"❌ Некоректні дані: {ke}")
    except Exception as e:
        await callback.message.edit_text(f"❌ Сталася помилка при збереженні: {e}")
    finally:
        await state.clear()


async def cancel_condition(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Додавання стану скасовано.")
    await state.clear()
