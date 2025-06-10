import psycopg2

db_connection = psycopg2.connect(
    dbname="farm_db",
    user="bot_user",
    password="Nazar0209",
    host="localhost",
    port="5432"
)
db_cursor = db_connection.cursor()

def fetch_all(query, params=None):
    try:
        db_cursor.execute(query, params or ())
        return db_cursor.fetchall()
    except Exception as e:
        print(f"❌ Помилка бази даних: {e}")
        return []

def execute_query(query, params=None):
    try:
        db_cursor.execute(query, params or ())
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        print(f"❌ Помилка виконання запиту: {e}")

def fetch_one(query, params=None):
    try:
        db_cursor.execute(query, params or ())
        return db_cursor.fetchone()
    except Exception as e:
        print(f"❌ Помилка бази даних: {e}")
        return None
