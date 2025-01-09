from aiogram.types import Message
from database import fetch_all


async def cmd_calculate_profit(message: Message):
    try:
        query = """
        SELECT c.id, c.name, 
               COALESCE(SUM(h.total_mass) * 1000, 0) AS total_income, 
               COALESCE(SUM(e.amount), 0) AS total_expenses, 
               COALESCE(SUM(h.total_mass) * 1000, 0) - COALESCE(SUM(e.amount), 0) AS profit
        FROM crops c
        LEFT JOIN harvest h ON c.id = h.crop_id
        LEFT JOIN expenses e ON c.id = e.crop_id
        GROUP BY c.id, c.name;
        """
        result = fetch_all(query)

        if not result:
            await message.reply("❌ Даних для розрахунку рентабельності немає.")
            return

        response = "📊 **Рентабельність посівів:**\n"
        for row in result:
            crop_id, name, income, expenses, profit = row
            response += (
                f"🌾 {name} (ID: {crop_id})\n"
                f"   Дохід: {income} грн\n"
                f"   Витрати: {expenses} грн\n"
                f"   Прибуток: {profit} грн\n\n"
            )

        await message.reply(response)
    except Exception as e:
        await message.reply(f"❌ Помилка при розрахунку рентабельності: {e}")
