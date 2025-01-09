import requests
from utils.config import OPENWEATHER_API

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API}&units=metric&lang=ua"
    response = requests.get(url)
    return response.json()
