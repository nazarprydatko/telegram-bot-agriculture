import uuid
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.weather_api import get_weather
from utils.logger_config import logger

class WeatherStates(StatesGroup):
    waiting_for_city = State()

async def cmd_get_weather(message: Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_city)
    await message.reply("🌆 Введіть назву міста, для якого хочете дізнатися погоду:")

async def process_city_weather(message: Message, state: FSMContext):
    try:
        city_name = message.text.strip()
        weather_data = get_weather(city_name)

        if weather_data.get("cod") != 200:
            await message.reply(f"❌ Помилка: {weather_data.get('message', 'Невідомо.')}")

        else:
            temp = weather_data['main']['temp']
            weather = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']

            response = (
                f"🌤 **Погода у місті {city_name.capitalize()}**:\n"
                f"🌡 Температура: {temp}°C\n"
                f"🌬 Вітер: {wind_speed} м/с\n"
                f"🌧 Опис: {weather.capitalize()}"
            )
            await message.reply(response)

    except Exception as e:
        error_id = str(uuid.uuid4())
        user_id = message.from_user.id

        logger.error(
            f"[ERROR_ID={error_id}] Помилка у process_city_weather для користувача {user_id}: {e}",
            exc_info=True
        )

        await message.reply(
            f"⚠️ Сталася технічна помилка.\nКод: `{error_id}`\nСпробуйте пізніше або зверніться до адміністратора."
        )

    finally:
        await state.clear()
