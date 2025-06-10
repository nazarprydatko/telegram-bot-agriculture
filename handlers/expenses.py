from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import execute_query

class ExpenseStates:
    waiting_for_expenses = "waiting_for_expenses"
    waiting_for_expense_confirmation = "waiting_for_expense_confirmation"

async def process_expense_data(message: Message, state: FSMContext):
    try:
        crop_id, category, amount_str = map(str.strip, message.text.split(","))
        crop_id = int(crop_id)
        amount = float(amount_str)

        if amount <= 0:
            raise ValueError("Сума витрат повинна бути більше 0.")

        # Зберігаємо у стан
        await state.update_data(
            crop_id=crop_id,
            category=category,
            amount=amount
        )

        text = (
            f"💰 Дані витрат:\n"
            f"ID посіву: {crop_id}\n"
            f"Категорія: {category}\n"
            f"Сума: {amount} грн\n\n"
            "✅ Підтвердити збереження?"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Так", callback_data="confirm_expense"),
             InlineKeyboardButton(text="❌ Ні", callback_data="cancel_expense")]
        ])
        await message.answer(text, reply_markup=keyboard)
        await state.set_state(ExpenseStates.waiting_for_expense_confirmation)

    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")

async def confirm_expense(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        execute_query(
            "INSERT INTO expenses (crop_id, category, amount) VALUES (%s, %s, %s);",
            (data["crop_id"], data["category"], data["amount"])
        )
        await callback.message.edit_text("✅ Витрати успішно додано!")
    except Exception as e:
        await callback.message.edit_text(f"❌ Помилка при збереженні: {e}")
    finally:
        await state.clear()

async def cancel_expense(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Додавання витрат скасовано.")
    await state.clear()
