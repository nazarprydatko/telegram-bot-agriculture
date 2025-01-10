import pytest
from unittest.mock import AsyncMock
from handlers.harvest import process_harvest_data
from database import execute_query, fetch_all
from datetime import date

@pytest.fixture
def mock_db():
    execute_query("DELETE FROM harvest;")
    execute_query("DELETE FROM crops;")
    execute_query("INSERT INTO crops (id, name, area, sowing_date, maturation_days) VALUES (1, 'Пшениця', 120, '2025-01-01', 120);")
    yield
    execute_query("DELETE FROM harvest;")
    execute_query("DELETE FROM crops;")

@pytest.mark.asyncio
async def test_add_valid_harvest(mock_db):
    message = AsyncMock()
    message.text = "1,2025-08-01,10,5000"
    message.reply = AsyncMock()
    state = AsyncMock()

    await process_harvest_data(message, state)

    # Перевірка відповіді
    message.reply.assert_called_with("✅ Врожай успішно додано для посіву 1!")

    result = fetch_all("SELECT crop_id, harvest_date, workers_count, total_mass FROM harvest;")
    assert result == [(1, date(2025, 8, 1), 10, 5000.0)]

@pytest.mark.asyncio
async def test_add_invalid_harvest(mock_db):
    message = AsyncMock()
    message.text = "1,2025-08-01,10,-5000"
    message.reply = AsyncMock()
    state = AsyncMock()

    await process_harvest_data(message, state)

    message.reply.assert_called_with("❌ Помилка у форматі введення: Маса врожаю повинна бути більше 0.")

    result = fetch_all("SELECT * FROM harvest;")
    assert result == []
