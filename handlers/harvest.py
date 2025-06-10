from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import execute_query

class HarvestStates:
    waiting_for_harvest = "waiting_for_harvest"
    waiting_for_harvest_confirmation = "waiting_for_harvest_confirmation"

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

        await state.update_data(
            crop_id=crop_id,
            harvest_date=harvest_date,
            workers_count=workers_count,
            total_mass=total_mass
        )

        # Підтвердження
        text = (
            f"🌾 Дані для врожаю:\n"
            f"ID посіву: {crop_id}\n"
            f"Дата: {harvest_date}\n"
            f"Працівників: {workers_count}\n"
            f"Маса: {total_mass} кг\n\n"
            "✅ Підтвердити збереження?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Так", callback_data="confirm_harvest"),
             InlineKeyboardButton(text="❌ Ні", callback_data="cancel_harvest")]
        ])
        await message.answer(text, reply_markup=keyboard)
        await state.set_state(HarvestStates.waiting_for_harvest_confirmation)

    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")

async def confirm_harvest(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        execute_query(
            "INSERT INTO harvest (crop_id, harvest_date, workers_count, total_mass) VALUES (%s, %s, %s, %s);",
            (data["crop_id"], data["harvest_date"], data["workers_count"], data["total_mass"])
        )
        await callback.message.edit_text("✅ Врожай успішно додано!")
    except Exception as e:
        await callback.message.edit_text(f"❌ Помилка при збереженні: {e}")
    finally:
        await state.clear()

async def cancel_harvest(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Додавання врожаю скасовано.")
    await state.clear()
