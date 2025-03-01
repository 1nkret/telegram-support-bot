from database.db import connect_db
from datetime import datetime

### ✅ CRUD for curator_requests (Student Requests)

def create_request(student_id: int, request_text: str) -> int:
    """Creates a new request in the database and returns its ID"""
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
    """Retrieves a request by ID"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_requests WHERE id = %s;", (request_id,))
    request = cursor.fetchone()

    cursor.close()
    conn.close()
    return request


def update_request_status(request_id: int, status: str, curator_id: int = None):
    """Updates the request status (and curator if needed)"""
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
    """Deletes a request from the database"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM curator_requests WHERE id = %s;", (request_id,))

    conn.commit()
    cursor.close()
    conn.close()


def get_active_requests():
    """Retrieves all active requests with status 'Pending processing'."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM curator_requests WHERE status IN (%s, %s, %s, %s);",
        ("Pending processing", "In progress", "Waiting", "Curator change")
    )
    active_requests = cursor.fetchall()

    cursor.close()
    conn.close()
    return active_requests


def get_closed_requests():
    """Retrieves all closed requests."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM curator_requests WHERE status IN (%s, %s);",
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
        "SELECT * FROM curator_requests WHERE id = %s;",
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
        UPDATE curator_requests
        SET thread_id = %s
        WHERE id = %s;
        """,
        (thread_id, request_id)
    )

    conn.commit()
    cursor.close()
    conn.close()


### ✅ CRUD for curator_logs (Curator Action Logs)

def log_action(request_id: int, curator_id: int, action: str):
    """Logs a curator's action"""
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
    """Retrieves all logs for a request"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_logs WHERE request_id = %s;", (request_id,))
    logs = cursor.fetchall()

    cursor.close()
    conn.close()
    return logs


### ✅ CRUD for curator_messages (Dialog Messages)

def add_message(request_id: int, sender_id: int, sender_role: str, message_text: str):
    """Adds a message to the dialog"""
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
    """Retrieves all messages in a dialog"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM curator_messages WHERE request_id = %s;", (request_id,))
    messages = cursor.fetchall()

    cursor.close()
    conn.close()
    return messages
