from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import fetch_all, execute_query
from datetime import datetime

class CropStates(StatesGroup):
    waiting_for_crop_data = State()
    waiting_for_crop_confirmation = State()

async def cmd_add_crop(message: Message, state: FSMContext):
    await message.reply(
        "Введіть дані для посіву: Назва культури, Площа (га), Дата посіву (YYYY-MM-DD), Прогноз дозрівання (днів)."
    )
    await state.set_state(CropStates.waiting_for_crop_data)

async def process_crop_data(message: Message, state: FSMContext):
    if message.text.strip() == "🏠 Головне меню":
        await state.clear()
        from handlers.start import cmd_start
        await cmd_start(message, state)
        return

    try:
        data = message.text.split(",")
        if len(data) != 4:
            await message.reply("❌ Некоректний формат. Введіть 4 значення через кому:\n"
                                "Назва, Площа (га), Дата (YYYY-MM-DD), Прогноз (днів).")
            return

        name, area_str, sowing_date_str, maturation_days_str = map(str.strip, data)

        try:
            area = float(area_str)
            if area <= 0:
                raise ValueError
        except ValueError:
            await message.reply("❌ Площа має бути додатнім числом (наприклад: 12.5).")
            return

        try:
            sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d")
            if sowing_date.date() > datetime.now().date():
                await message.reply("❌ Дата посіву не може бути в майбутньому.")
                return
        except ValueError:
            await message.reply("❌ Невірний формат дати. Використовуйте YYYY-MM-DD.")
            return

        try:
            maturation_days = int(maturation_days_str)
            if maturation_days <= 0:
                raise ValueError
        except ValueError:
            await message.reply("❌ Прогноз дозрівання має бути цілим додатнім числом (наприклад: 90).")
            return

        await state.update_data(
            name=name,
            area=area,
            sowing_date=sowing_date_str,
            maturation_days=maturation_days
        )

        summary = (
            f"🌾 Дані для посіву:\n"
            f"Назва: {name}\n"
            f"Площа: {area} га\n"
            f"Дата: {sowing_date_str}\n"
            f"Дозрівання: {maturation_days} днів\n\n"
            "Підтвердити збереження?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Так", callback_data="confirm_crop"),
             InlineKeyboardButton(text="❌ Ні", callback_data="cancel_crop")]
        ])
        await message.answer(summary, reply_markup=keyboard)
        await state.set_state(CropStates.waiting_for_crop_confirmation)

    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")

async def confirm_crop(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        query = """
        INSERT INTO crops (name, area, sowing_date, maturation_days)
        VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (
            data["name"],
            data["area"],
            data["sowing_date"],
            data["maturation_days"]
        ))
        await callback.message.edit_text("✅ Посів успішно додано!")
    except Exception as e:
        await callback.message.edit_text(f"❌ Помилка при збереженні: {e}")
    finally:
        await state.clear()

async def cancel_crop(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Додавання посіву скасовано.")
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
