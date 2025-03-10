import psycopg2
from psycopg2.extras import DictCursor
from core.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    """Создает базу данных, если её нет"""
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database {DB_NAME} is successful created.")

    cursor.close()
    conn.close()


def connect_db():
    """Создает подключение к БД"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        cursor_factory=DictCursor
    )


def create_tables():
    """Создает таблицы в БД"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        -- Таблица запросов (диалогов)
        CREATE TABLE IF NOT EXISTS support_requests (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            request_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            status TEXT DEFAULT 'Pending processing',
            support_id BIGINT DEFAULT NULL,
            taken_at TIMESTAMP DEFAULT NULL,
            thread_id INTEGER
        );

        -- Таблица логов действий кураторов
        CREATE TABLE IF NOT EXISTS support_logs (
            id SERIAL PRIMARY KEY,
            request_id INT REFERENCES support_requests(id) ON DELETE CASCADE,
            support_id BIGINT NOT NULL,
            action TEXT NOT NULL,
            action_time TIMESTAMP DEFAULT NOW()
        );

        -- Таблица сообщений в диалогах
        CREATE TABLE IF NOT EXISTS support_messages (
            id SERIAL PRIMARY KEY,
            request_id INT REFERENCES support_requests(id) ON DELETE CASCADE,
            sender_id BIGINT NOT NULL,
            sender_role TEXT NOT NULL,
            message_text TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
    create_tables()
