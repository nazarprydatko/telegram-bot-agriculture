from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import fetch_one, fetch_all, execute_query

class EditCropStates(StatesGroup):
    waiting_for_crop_id = State()
    waiting_for_new_data = State()
    waiting_for_confirmation = State()

# Кнопка редагування посіву
async def callback_edit_crop(callback: CallbackQuery, state: FSMContext):
    try:
        crops = fetch_all("SELECT id, name FROM crops")
        if not crops:
            await callback.message.answer("❌ Посівів немає для редагування.")
            return

        response = "✏️ *Оберіть ID посіву для редагування:*\n"
        for crop in crops:
            response += f"ID: {crop[0]}, Назва: {crop[1]}\n"

        await callback.message.answer(response)
        await callback.message.answer("Введіть ID посіву:")
        await state.set_state(EditCropStates.waiting_for_crop_id)
    except Exception as e:
        await callback.message.answer(f"❌ Помилка: {e}")

# Отримання ID і  даних
async def process_edit_crop_id(message: Message, state: FSMContext):
    if message.text.strip() == "🏠 Головне меню":
        await state.clear()
        from handlers.start import cmd_start
        await cmd_start(message, state)
        return

    try:
        crop_id = int(message.text.strip())
        result = fetch_one("SELECT name, area, sowing_date, maturation_days FROM crops WHERE id = %s", (crop_id,))
        if not result:
            await message.reply("❌ Посів з таким ID не знайдено.")
            return

        await state.update_data(crop_id=crop_id)
        await message.reply(
            f"Поточні дані:\nНазва: {result[0]}\nПлоща: {result[1]} га\nДата посіву: {result[2]}\nПрогноз: {result[3]} днів"
        )
        await message.reply(
            "Введіть нові дані у форматі: Назва, Площа (га), Дата (YYYY-MM-DD), Прогноз дозрівання (днів)."
        )
        await state.set_state(EditCropStates.waiting_for_new_data)
    except ValueError:
        await message.reply("❌ Введіть коректне число (ID).")

# Обробка нових дата підтвердження
async def process_edit_crop_data(message: Message, state: FSMContext):
    if message.text.strip() == "🏠 Головне меню":
        await state.clear()
        from handlers.start import cmd_start
        await cmd_start(message, state)
        return

    try:
        data = message.text.split(",")
        if len(data) != 4:
            await message.reply("❌ Формат: Назва, Площа, Дата, Прогноз.")
            return

        name, area_str, date_str, maturation_str = map(str.strip, data)
        area = float(area_str)
        maturation = int(maturation_str)

        if area <= 0 or maturation <= 0:
            raise ValueError("Значення повинні бути додатними.")

        await state.update_data(
            new_name=name,
            new_area=area,
            new_date=date_str,
            new_maturation=maturation
        )

        confirm_text = (
            f"🔄 Нові дані:\n"
            f"Назва: {name}\n"
            f"Площа: {area} га\n"
            f"Дата: {date_str}\n"
            f"Прогноз: {maturation} днів\n\n"
            "Підтвердити оновлення?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Так", callback_data="confirm_crop_edit"),
             InlineKeyboardButton(text="❌ Ні", callback_data="cancel_crop_edit")]
        ])
        await message.answer(confirm_text, reply_markup=keyboard)
        await state.set_state(EditCropStates.waiting_for_confirmation)

    except Exception as e:
        await message.reply(f"❌ Помилка: {e}")

# Підтвердження
async def confirm_crop_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        execute_query(
            "UPDATE crops SET name=%s, area=%s, sowing_date=%s, maturation_days=%s WHERE id=%s",
            (data["new_name"], data["new_area"], data["new_date"], data["new_maturation"], data["crop_id"])
        )
        await callback.message.edit_text("✅ Посів успішно оновлено!")
    except Exception as e:
        await callback.message.edit_text(f"❌ Помилка при оновленні: {e}")
    finally:
        await state.clear()

# Відміна
async def cancel_crop_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Редагування скасовано.")
    await state.clear()
