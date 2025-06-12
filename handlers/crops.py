from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import fetch_all, execute_query
from datetime import datetime
import uuid
from utils.logger_config import logger

class CropStates(StatesGroup):
    """
    States for managing crop-related user input.
    """
    waiting_for_crop_data = State()
    waiting_for_crop_confirmation = State()


async def cmd_add_crop(message: Message, state: FSMContext):
    """
    Ask the user to input crop data and set the FSM state.

    Args:
        message (Message): The Telegram message that triggered the command.
        state (FSMContext): The FSM context to manage state transitions.

    Returns:
        None
    """
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
            error_id = str(uuid.uuid4())
            user_id = message.from_user.id
            logger.warning(
                f"[ERROR_ID={error_id}] Неправильна кількість параметрів у process_crop_data від користувача {user_id}: {data}",
                exc_info=True
            )
            await message.reply(
                f"❌ Некоректний формат. Введіть 4 значення через кому:\n"
                f"Назва, Площа (га), Дата (YYYY-MM-DD), Прогноз (днів).\nКод помилки: `{error_id}`"
            )
            return

        name, area_str, sowing_date_str, maturation_days_str = map(str.strip, data)

        try:
            area = float(area_str)
            if area <= 0:
                raise ValueError
        except ValueError:
            error_id = str(uuid.uuid4())
            user_id = message.from_user.id
            logger.warning(
                f"[ERROR_ID={error_id}] Некоректна площа в process_crop_data від користувача {user_id}: {area_str}",
                exc_info=True
            )
            await message.reply(
                f"❌ Площа має бути додатнім числом (наприклад: 12.5).\nКод помилки: `{error_id}`"
            )
            return

        try:
            sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d")
            if sowing_date.date() > datetime.now().date():
                error_id = str(uuid.uuid4())
                user_id = message.from_user.id
                logger.warning(
                    f"[ERROR_ID={error_id}] Дата посіву в майбутньому від користувача {user_id}: {sowing_date_str}",
                    exc_info=True
                )
                await message.reply(
                    f"❌ Дата посіву не може бути в майбутньому.\nКод помилки: `{error_id}`"
                )
                return
        except ValueError:
            error_id = str(uuid.uuid4())
            user_id = message.from_user.id
            logger.warning(
                f"[ERROR_ID={error_id}] Невалідна дата у process_crop_data від користувача {user_id}: {sowing_date_str}",
                exc_info=True
            )
            await message.reply(
                f"❌ Невірний формат дати. Використовуйте YYYY-MM-DD.\nКод помилки: `{error_id}`"
            )
            return

        try:
            maturation_days = int(maturation_days_str)
            if maturation_days <= 0:
                raise ValueError
        except ValueError:
            error_id = str(uuid.uuid4())
            user_id = message.from_user.id
            logger.warning(
                f"[ERROR_ID={error_id}] Невалідне число днів дозрівання в process_crop_data від користувача {user_id}: {maturation_days_str}",
                exc_info=True
            )
            await message.reply(
                f"❌ Прогноз дозрівання має бути цілим додатнім числом (наприклад: 90).\nКод помилки: `{error_id}`"
            )
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

    except (ValueError, TypeError, KeyError) as e:
        error_id = str(uuid.uuid4())
        user_id = message.from_user.id
        logger.warning(
            f"[ERROR_ID={error_id}] Помилка валідації в process_crop_data від користувача {user_id}: {e}",
            exc_info=True
        )
        await message.reply(
            f"❌ Введені дані некоректні. Код помилки: `{error_id}`"
        )

    except Exception as e:
        error_id = str(uuid.uuid4())
        user_id = message.from_user.id
        logger.error(
            f"[ERROR_ID={error_id}] Невідома помилка в process_crop_data від користувача {user_id}: {e}",
            exc_info=True
        )
        await message.reply(
            f"⚠️ Сталася технічна помилка.\nКод: `{error_id}`\nСпробуйте пізніше або зверніться до адміністратора."
        )


async def confirm_crop(callback: CallbackQuery, state: FSMContext):
    """
    Save the confirmed crop data to the database.

    Args:
        callback (CallbackQuery): Callback from inline button.
        state (FSMContext): FSM context with previously stored crop data.

    Returns:
        None
    """
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

    except KeyError as ke:
        error_id = str(uuid.uuid4())
        logger.warning(
            f"[ERROR_ID={error_id}] Відсутній ключ у confirm_crop: {ke}",
            exc_info=True
        )
        await callback.message.edit_text(
            f"❌ Помилка структури даних. Код: `{error_id}`"
        )

    except Exception as e:
        error_id = str(uuid.uuid4())
        logger.error(
            f"[ERROR_ID={error_id}] Помилка запису до БД у confirm_crop: {e}",
            exc_info=True
        )
        await callback.message.edit_text(
            f"⚠️ Сталася технічна помилка при збереженні.\nКод: `{error_id}`"
        )

    finally:
        await state.clear()


async def cancel_crop(callback: CallbackQuery, state: FSMContext):
    """
    Cancel crop creation and clear the state.

    Args:
        callback (CallbackQuery): Callback from inline button.
        state (FSMContext): FSM context to clear data.

    Returns:
        None
    """
    await callback.message.edit_text("❌ Додавання посіву скасовано.")
    await state.clear()


async def callback_view_crops(callback: CallbackQuery):
    """
    Display a list of all crops from the database.

    Args:
        callback (CallbackQuery): Callback from user requesting crop list.

    Returns:
        None
    """
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
        error_id = str(uuid.uuid4())
        logger.error(
            f"[ERROR_ID={error_id}] Помилка у callback_view_crops: {e}",
            exc_info=True
        )
        await callback.message.answer(
            f"⚠️ Помилка при отриманні списку посівів.\nКод: `{error_id}`"
        )

