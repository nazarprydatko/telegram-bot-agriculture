@echo off
echo  Активую віртуальне середовище...
call .env\Scripts\activate.bat

echo  Запускаю Telegram-бота...
python bot.py

pause
