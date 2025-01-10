from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import execute_query

async def process_expense_data(message: Message, state: FSMContext):
    try:
        # Розділення вхідного тексту
        crop_id, category, amount = map(str.strip, message.text.split(","))
        crop_id = int(crop_id)
        amount = float(amount)

        # Перевірка суми витрат
        if amount <= 0:
            raise ValueError("Сума витрат не може бути від'ємною або рівною нулю.")

        # Вставка даних у базу
        execute_query(
            "INSERT INTO expenses (crop_id, category, amount) VALUES (%s, %s, %s);",
            (crop_id, category, amount)
        )
        await message.reply(f"✅ Витрати успішно додано для посіву {crop_id}!")
    except ValueError as ve:
        await message.reply(f"❌ Помилка у форматі введення: {ve}")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")
    finally:
        await state.clear()
