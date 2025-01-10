import pytest
from unittest.mock import AsyncMock
from handlers.conditions import process_condition_data
from database import execute_query, fetch_all

@pytest.fixture
def mock_db():
    execute_query("DELETE FROM crop_conditions;")
    execute_query("DELETE FROM crops;")
    execute_query("INSERT INTO crops (id, name, area, sowing_date, maturation_days) VALUES (1, 'Пшениця', 120, '2025-01-01', 120);")
    yield
    execute_query("DELETE FROM crop_conditions;")
    execute_query("DELETE FROM crops;")

@pytest.mark.asyncio
async def test_add_valid_condition(mock_db):
    message = AsyncMock()
    message.text = "1,50,20,5"
    message.reply = AsyncMock()

    await process_condition_data(message)

    message.reply.assert_called_with("✅ Дані стану для посіву ID 1 успішно додано!")

    result = fetch_all("SELECT crop_id, soil_moisture, temperature, precipitation FROM crop_conditions;")
    assert result == [(1, 50.0, 20.0, 5.0)]

@pytest.mark.asyncio
async def test_add_invalid_condition(mock_db):

    message = AsyncMock()
    message.text = "1,150,20,5"
    message.reply = AsyncMock()

    await process_condition_data(message)

    message.reply.assert_called_with("❌ Помилка у форматі введення: Вологість повинна бути в межах 0-100%.")

    result = fetch_all("SELECT * FROM crop_conditions;")
    assert result == []
