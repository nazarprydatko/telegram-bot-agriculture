@echo off
echo  Отримую останні зміни з Git...
git pull origin main

echo  Активую середовище...
call venv\Scripts\activate.bat

echo  Оновлюю залежності...
pip install -r requirements.txt

echo  Перезапускаю бота...
taskkill /F /IM python.exe
start python main.py

echo  Деплой завершено.

pause
