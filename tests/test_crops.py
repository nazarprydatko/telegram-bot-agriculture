import pytest
from unittest.mock import AsyncMock
from handlers.crops import process_crop_data
from database import execute_query, fetch_all


@pytest.fixture
def mock_db():
    execute_query("DELETE FROM crops;")
    yield
    execute_query("DELETE FROM crops;")


@pytest.mark.asyncio
async def test_add_valid_crop(mock_db):
    message = AsyncMock()
    message.text = "Пшениця,120,2025-01-01,120"
    message.reply = AsyncMock()

    await process_crop_data(message, None)

    message.reply.assert_called_with("✅ Дані для посіву 'Пшениця' успішно додано!")

    result = fetch_all("SELECT name, area, sowing_date, maturation_days FROM crops;")
    result = [(name, area, str(sowing_date), maturation_days) for name, area, sowing_date, maturation_days in result]
    assert result == [("Пшениця", 120.0, "2025-01-01", 120)]


@pytest.mark.asyncio
async def test_add_invalid_crop(mock_db):
    message = AsyncMock()
    message.text = "Кукурудза,-1,2025-01-01,100"
    message.reply = AsyncMock()

    await process_crop_data(message, None)

    message.reply.assert_called_with("❌ Помилка у форматі введення: Площа не може бути від'ємною або рівною нулю.")


    result = fetch_all("SELECT * FROM crops;")
    assert result == []
