# Інструкція з розгортання Telegram-бота у production

## 1. Передумови

Перед розгортанням необхідно мати:

- Сервер (VPS або локальний) з Linux (Ubuntu 20.04+)
- Python 3.12+
- PostgreSQL (версія 13+)
- Доступ до Telegram Bot Token
- Git

## 2. Клонування репозиторію

```
git clone https://github.com/your-username/telegram-bot-agriculture.git
cd telegram-bot-agriculture 
```
## 3. Налаштування середовища

``` 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 4. Створення бази даних PostgreSQL

```
sudo -u postgres psql
CREATE DATABASE agro_db;
CREATE USER agro_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE agro_db TO agro_user;
```

## 5. Налаштування змінних середовища
створіть енв файл 
```
API_TOKEN=токен_вашого_бота
DB_HOST=localhost
DB_NAME=agro_db
DB_USER=agro_user
DB_PASSWORD=secure_password
```

## 6. Запуск бота як сервісу
```
bash docs/scripts/start.sh
```
## 7. Рекомендації з безпеки

Змініть паролі за замовчуванням

Обмежте доступ до .env

Налаштуйте firewall

Регулярно оновлюйте залежності