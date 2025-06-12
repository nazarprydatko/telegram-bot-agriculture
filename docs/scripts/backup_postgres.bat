@echo off
setlocal enabledelayedexpansion

REM Отримання дати у форматі YYYY-MM-DD
for /f %%a in ('wmic os get LocalDateTime ^| find "."') do set dt=%%a
set DATE=!dt:~0,4!-!dt:~4,2!-!dt:~6,2!

echo  Створюю резервну копію бази agro_db...
pg_dump -U agro_user -d agro_db > backup_!DATE!.sql

echo  Backup created: backup_!DATE!.sql

pause
