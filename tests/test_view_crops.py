import pytest
from unittest.mock import AsyncMock
from handlers.crops import callback_view_crops
from database import execute_query

@pytest.fixture
def mock_db():
    execute_query("DELETE FROM crops;")
    execute_query("INSERT INTO crops (id, name, area, sowing_date, maturation_days) VALUES (1, 'Пшениця', 120, '2025-01-01', 120);")
    execute_query("INSERT INTO crops (id, name, area, sowing_date, maturation_days) VALUES (2, 'Кукурудза', 150, '2025-02-01', 100);")
    yield
    execute_query("DELETE FROM crops;")

@pytest.mark.asyncio
async def test_view_crops(mock_db):
    callback = AsyncMock()
    callback.message.answer = AsyncMock()

    await callback_view_crops(callback)

    expected_response = (
        "🌾 **Список посівів:**\n"
        "ID: 1, Назва: Пшениця, Площа: 120.0 га, Дата посіву: 2025-01-01\n"
        "ID: 2, Назва: Кукурудза, Площа: 150.0 га, Дата посіву: 2025-02-01\n"
    )
    callback.message.answer.assert_called_with(expected_response)