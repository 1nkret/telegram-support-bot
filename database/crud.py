from database.db import connect_db
from datetime import datetime


def create_request(user_id: int, request_text: str) -> int:
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO support_requests (user_id, request_text, created_at)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (user_id, request_text, datetime.now()))

    request_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return request_id


def get_request(request_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM support_requests WHERE id = %s;", (request_id,))
    request = cursor.fetchone()

    cursor.close()
    conn.close()
    return request


def update_request_status(request_id: int, status: str, support_id: int = None):
    conn = connect_db()
    cursor = conn.cursor()

    if support_id:
        cursor.execute("""
            UPDATE support_requests
            SET status = %s, support_id = %s, taken_at = %s
            WHERE id = %s;
        """, (status, support_id, datetime.now(), request_id))
    else:
        cursor.execute("""
            UPDATE support_requests
            SET status = %s
            WHERE id = %s;
        """, (status, request_id))

    conn.commit()
    cursor.close()
    conn.close()


def delete_request(request_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM support_requests WHERE id = %s;", (request_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_active_requests():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM support_requests WHERE status IN (%s, %s, %s, %s);",
        ("Pending processing", "In progress", "Waiting", "Support change")
    )
    active_requests = cursor.fetchall()

    cursor.close()
    conn.close()
    return active_requests


def get_closed_requests():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM support_requests WHERE status IN (%s, %s);",
        ("Cancelled", "Completed")
    )
    closed_requests = cursor.fetchall()

    cursor.close()
    conn.close()
    return closed_requests


def get_thread_id(request_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM support_requests WHERE id = %s;",
        (request_id,)
    )

    active_requests = cursor.fetchall()

    cursor.close()
    conn.close()

    if active_requests:
        return active_requests[0]
    return tuple()


def update_thread_id(request_id, thread_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE support_requests
        SET thread_id = %s
        WHERE id = %s;
        """,
        (thread_id, request_id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def log_action(request_id: int, support_id: int, action: str):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO support_logs (request_id, support_id, action, action_time)
        VALUES (%s, %s, %s, %s);
    """, (request_id, support_id, action, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()


def get_logs(request_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM support_logs WHERE request_id = %s;", (request_id,))
    logs = cursor.fetchall()

    cursor.close()
    conn.close()
    return logs


def add_message(request_id: int, sender_id: int, sender_role: str, message_text: str):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO support_messages (request_id, sender_id, sender_role, message_text, sent_at)
        VALUES (%s, %s, %s, %s, %s);
    """, (request_id, sender_id, sender_role, message_text, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()


def get_messages(request_id: int):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM support_messages WHERE request_id = %s;", (request_id,))
    messages = cursor.fetchall()

    cursor.close()
    conn.close()
    return messages
