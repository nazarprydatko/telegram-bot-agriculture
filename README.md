Telegram-Bot for Agriculture Management

## Опис проекту
Цей Telegram-бот призначений для аграрних підприємств. Він допомагає автоматизувати управління культурами, витратами, врожаєм, та генерувати звіти. Бот інтегрується з OpenWeatherMap API для отримання актуальної погоди та містить зручний інтерфейс для роботи.


1. Облік культур
   - Додавання нових культур (назва, площа, дата посіву, прогноз дозрівання).
   - Перегляд та видалення існуючих культур.

2. Стан посівів
   - Запис даних про вологість ґрунту, температуру, опади.

3. Врожай
   - Внесення даних про дату збору, масу врожаю, кількість працівників.

4. Витрати
   - Запис витрат за категоріями (добрива, техніка тощо).

5. Рентабельність
   - Розрахунок прибутковості культур на основі доходів і витрат.

6. Погодні дані
   - Отримання прогнозів погоди для будь-якого міста.

7. Генерація звітів
   - Формування звітів у форматах PDF та Excel.


 Структура проекту
- `bot.py`
  Головний файл запуску бота.
- `database.py`  
  Модуль для роботи з базою даних PostgreSQL.
- `handlers/`
  Папка з обробниками команд:
  - `conditions.py` – стан посівів.
  - `crops.py` – облік культур.
  - `delete.py` – видалення даних.
  - `expenses.py` – витрати.
  - `harvest.py` – врожай.
  - `profit.py` – рентабельність.
  - `reports.py` – генерація звітів.
  - `start.py` – головне меню.
  - `weather.py` – погодні дані.
- `utils/` 
  Утиліти:
  - `config.py` – конфігурація.
  - `excel_generator.py` – генерація Excel-звітів.
  - `pdf_generator.py` – генерація PDF-звітів.
  - `weather_api.py` – інтеграція з OpenWeatherMap.


Як встановити
1. Склонуйте репозиторій:
   ```bash
   git clone https://github.com/nazarprydatko/telegram-bot-agriculture.git
   cd telegram-bot-agriculture
2. Створіть та активуйте віртуальне середовище:
   python -m venv .venv
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate    # Windows

3. Встановіть залежності
   pip install -r requirements.txt

4. Налаштуйте конфігурацію в utils/config.py
    Вкажіть API_TOKEN для Telegram.
    Додайте налаштування для PostgreSQL.
    Введіть API ключ OpenWeatherMap.

5.Запустіть бота 
    python bot.py

## Документування коду

Для підтримки єдиного стилю в проєкті використовується форматування Google-style docstrings.

### Приклад:
```python
def calculate_profit(revenue: float, expenses: float) -> float:
    """
    Обчислює прибуток за доходом та витратами.

    Args:
        revenue (float): Сума доходу.
        expenses (float): Сума витрат.

    Returns:
        float: Чистий прибуток.
    """
