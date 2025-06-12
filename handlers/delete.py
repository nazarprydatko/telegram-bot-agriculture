from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import execute_query

class DeleteStates(StatesGroup):
    waiting_for_crop_id = State()
    confirm_deletion = State()


async def cmd_delete_data(message: Message, state: FSMContext):
    await state.set_state(DeleteStates.waiting_for_crop_id)
    await message.reply("🔢 Введіть ID посіву, який потрібно видалити:")


async def process_delete_data(message: Message, state: FSMContext):
    try:
        crop_id = int(message.text.strip())
        await state.update_data(crop_id=crop_id)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm_delete"),
                    InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_delete"),
                ]
            ]
        )
        await message.reply(f"⚠️ Ви впевнені, що хочете видалити посів з ID {crop_id}?", reply_markup=keyboard)
        await state.set_state(DeleteStates.confirm_deletion)

    except ValueError:
        await message.reply("❌ ID має бути числом. Спробуйте ще раз.")
    except Exception as e:
        await message.reply(f"❌ Неочікувана помилка: {e}")


async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        crop_id = data.get("crop_id")
        execute_query("DELETE FROM crops WHERE id = %s", (crop_id,))
        await callback.message.edit_text(f"✅ Дані посіву з ID {crop_id} успішно видалено!")
    except KeyError as ke:
        await callback.message.edit_text(f"❌ Помилка: відсутній crop_id: {ke}")
    except Exception as e:
        await callback.message.edit_text(f"❌ Сталася помилка: {e}")
    finally:
        await state.clear()


async def cancel_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Видалення скасовано.")
    await state.clear()
