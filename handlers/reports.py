from aiogram.types import Message, FSInputFile
from database import fetch_all
from utils.excel_generator import generate_excel
from aiogram.filters import Command

async def cmd_generate_report(message: Message):
    try:
        query = "SELECT name, area, sowing_date, maturation_days FROM crops;"
        data = fetch_all(query)
        formatted_data = [
            {"culture": row[0], "area": row[1], "sowing_date": row[2], "maturation_days": row[3]}
            for row in data
        ]
        from utils.pdf_generator import generate_pdf
        generate_pdf(formatted_data)
        pdf_file = FSInputFile("report.pdf")
        await message.answer_document(pdf_file, caption="Ось ваш звіт у форматі PDF.")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка при генерації PDF-звіту: {e}")

async def cmd_export_to_excel(message: Message):
    try:
        query = "SELECT * FROM crops;"
        data = fetch_all(query)

        file_path = generate_excel(data)

        excel_file = FSInputFile(file_path)
        await message.answer_document(excel_file, caption="Ось ваш звіт у форматі Excel.")
    except Exception as e:
        await message.reply(f"❌ Сталася помилка при генерації Excel-звіту: {e}")
