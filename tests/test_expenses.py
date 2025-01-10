import pytest
from unittest.mock import AsyncMock
from handlers.expenses import process_expense_data
from database import execute_query, fetch_all

@pytest.fixture
def mock_db():
    execute_query("DELETE FROM expenses;")
    execute_query("DELETE FROM crops;")
    execute_query("INSERT INTO crops (id, name, area, sowing_date, maturation_days) VALUES (1, 'Пшениця', 120, '2025-01-01', 120);")
    yield
    execute_query("DELETE FROM expenses;")
    execute_query("DELETE FROM crops;")

@pytest.mark.asyncio
async def test_add_valid_expense(mock_db):
    message = AsyncMock()
    message.text = "1,Добрива,5000"
    message.reply = AsyncMock()
    state = AsyncMock()

    await process_expense_data(message, state)

    message.reply.assert_called_with("✅ Витрати успішно додано для посіву 1!")

    result = fetch_all("SELECT crop_id, category, amount FROM expenses;")
    assert result == [(1, "Добрива", 5000.0)]

@pytest.mark.asyncio
async def test_add_invalid_expense(mock_db):
    message = AsyncMock()
    message.text = "1,Добрива,-5000"
    message.reply = AsyncMock()
    state = AsyncMock()

    await process_expense_data(message, state)

    message.reply.assert_called_with("❌ Помилка у форматі введення: Сума витрат не може бути від'ємною або рівною нулю.")

    result = fetch_all("SELECT * FROM expenses;")
    assert result == []
