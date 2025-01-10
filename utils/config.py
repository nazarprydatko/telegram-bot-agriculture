import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in the environment variables!")

DB_CONFIG = {
    "dbname": "farm_db",
    "user": "bot_user",
    "password": "Nazar0209",
    "host": "localhost",
    "port": "5432"
}

OPENWEATHER_API = "2367f3a0f6f1f7f170022a9aa93f8f5b"
