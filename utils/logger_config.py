import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Конфігурація логування
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),   # запис
        logging.StreamHandler()
    ]
)

# Створення іменованого логера
logger = logging.getLogger("telegram_bot")
