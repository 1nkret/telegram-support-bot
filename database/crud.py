from database.db import connect_db
from datetime import datetime


### ✅ CRUD для curator_requests (Запросы учеников)

def create_request(student_id: int, request_text: str) -> int:
    """Создает новый запрос в БД и возвращает его ID"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO curator_requests (student_id, request_text, created_at)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (student_id, request_text, datetime.now()))

    request_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return request_id


def get_request(request_id: int):
    """Получает запрос по ID"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_requests WHERE id = %s;", (request_id,))
    request = cursor.fetchone()

    cursor.close()
    conn.close()
    return request


def update_request_status(request_id: int, status: str, curator_id: int = None):
    """Обновляет статус запроса (и куратора, если нужно)"""
    conn = connect_db()
    cursor = conn.cursor()

    if curator_id:
        cursor.execute("""
            UPDATE curator_requests
            SET status = %s, curator_id = %s, taken_at = %s
            WHERE id = %s;
        """, (status, curator_id, datetime.now(), request_id))
    else:
        cursor.execute("""
            UPDATE curator_requests
            SET status = %s
            WHERE id = %s;
        """, (status, request_id))

    conn.commit()
    cursor.close()
    conn.close()


def delete_request(request_id: int):
    """Удаляет запрос из базы"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM curator_requests WHERE id = %s;", (request_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_active_requests():
    """Получает все активные запросы со статусом 'Ожидает обработки...'."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM curator_requests WHERE status IN (%s, %s, %s, %s);",
        ("Ожидает обработки", "В роботі", "Очікує", "Зміна куратора")
    )
    active_requests = cursor.fetchall()  # Получаем все записи

    cursor.close()
    conn.close()
    return active_requests


def get_closed_requests():
    """Получает все активные запросы со статусом 'Ожидает обработки...'."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM curator_requests WHERE status IN (%s, %s);",
        ("Скасовано", "Виконано")
    )
    active_requests = cursor.fetchall()  # Получаем все записи

    cursor.close()
    conn.close()
    return active_requests


### ✅ CRUD для curator_logs (Логирование действий кураторов)

def log_action(request_id: int, curator_id: int, action: str):
    """Логирует действие куратора"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO curator_logs (request_id, curator_id, action, action_time)
        VALUES (%s, %s, %s, %s);
    """, (request_id, curator_id, action, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()


def get_logs(request_id: int):
    """Получает все логи по запросу"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_logs WHERE request_id = %s;", (request_id,))
    logs = cursor.fetchall()

    cursor.close()
    conn.close()
    return logs


### ✅ CRUD для curator_messages (Сообщения в диалогах)

def add_message(request_id: int, sender_id: int, sender_role: str, message_text: str):
    """Добавляет сообщение в диалог"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO curator_messages (request_id, sender_id, sender_role, message_text, sent_at)
        VALUES (%s, %s, %s, %s, %s);
    """, (request_id, sender_id, sender_role, message_text, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()


def get_messages(request_id: int):
    """Получает всю переписку в диалоге"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_messages WHERE request_id = %s;", (request_id,))
    messages = cursor.fetchall()

    cursor.close()
    conn.close()
    return messages
