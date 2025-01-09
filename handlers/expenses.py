from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database import execute_query

async def process_expense_data(message: Message, state: FSMContext):
    try:
        crop_id, category, amount = map(str.strip, message.text.split(","))
        crop_id = int(crop_id)
        amount = float(amount)

        execute_query(
            "INSERT INTO expenses (crop_id, category, amount) VALUES (%s, %s, %s);",
            (crop_id, category, amount)
        )
        await message.reply(f"✅ Витрати успішно додано для посіву {crop_id}!")
    except ValueError:
        await message.reply("❌ Неправильний формат. Введіть: ID посіву, Категорія витрат, Сума.")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка: {e}")
    finally:
        await state.clear()
