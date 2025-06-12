from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database import execute_query

class ExpenseStates:
    """
    FSM states for managing expense input and confirmation.
    """
    waiting_for_expenses = "waiting_for_expenses"
    waiting_for_expense_confirmation = "waiting_for_expense_confirmation"


async def process_expense_data(message: Message, state: FSMContext):
    """
    Process user input for expenses and prepare confirmation message.

    Expected input format: crop_id, category, amount

    Args:
        message (Message): User message containing expense data.
        state (FSMContext): FSM context to store parsed data.

    Returns:
        None
    """
    try:
        crop_id, category, amount_str = map(str.strip, message.text.split(","))
        crop_id = int(crop_id)
        amount = float(amount_str)

        if amount <= 0:
            raise ValueError("Сума витрат повинна бути більше 0.")

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
    except (TypeError, KeyError) as e:
        await message.reply(f"❌ Невірні або відсутні дані: {e}")
    except Exception as e:
        await message.reply(f"❌ Неочікувана помилка: {e}")


async def confirm_expense(callback: CallbackQuery, state: FSMContext):
    """
    Save confirmed expense data to the database.

    Args:
        callback (CallbackQuery): Callback from inline button.
        state (FSMContext): FSM context containing previously entered expense data.

    Returns:
        None
    """
    data = await state.get_data()
    try:
        execute_query(
            "INSERT INTO expenses (crop_id, category, amount) VALUES (%s, %s, %s);",
            (data["crop_id"], data["category"], data["amount"])
        )
        await callback.message.edit_text("✅ Витрати успішно додано!")
    except KeyError as ke:
        await callback.message.edit_text(f"❌ Некоректні ключі в даних: {ke}")
    except Exception as e:
        await callback.message.edit_text(f"❌ Помилка при збереженні: {e}")
    finally:
        await state.clear()


async def cancel_expense(callback: CallbackQuery, state: FSMContext):
    """
    Cancel the expense addition process and clear FSM state.

    Args:
        callback (CallbackQuery): Callback from inline button.
        state (FSMContext): FSM context to clear.

    Returns:
        None
    """
    await callback.message.edit_text("❌ Додавання витрат скасовано.")
    await state.clear()
