import psycopg2
from ..settings import DB_CONFIG

def create_task_comment(task_id, user_id, comment):
    query = """
        INSERT INTO task_comments (task_id, user_id, comment)
        VALUES (%s, %s, %s)
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (task_id, user_id, comment))
    conn.commit()

    cursor.close()
    conn.close()

def edit_task_comment(task_id, user_id, comment):
    query_check = """
    SELECT id FROM task_comments WHERE task_id = %s AND user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query_check, (task_id, user_id))
    comment_id = cursor.fetchone()

    if comment_id:
        query = """
        UPDATE task_comments
        SET comment = %s
        WHERE id = %s
        """
        cursor.execute(query, (comment, comment_id[0]))
        conn.commit()
    else:
        query = """
        INSERT INTO task_comments (task_id, user_id, comment)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (task_id, user_id, comment))
        conn.commit()

    cursor.close()
    conn.close()

def delete_task_comment(task_id, user_id=None, comment_id=None):
    """
    Удаляет комментарий для задачи:
    - Если user_id и comment_id указаны, удаляет конкретный комментарий пользователя.
    - Если только task_id, удаляет все комментарии для этой задачи.
    - Если только user_id, удаляет все комментарии этого пользователя для задачи.
    """
    if user_id is None and comment_id is None:
        # Удаляем все комментарии для задачи
        query = """
        DELETE FROM task_comments
        WHERE task_id = %s
        """
        params = (task_id,)
    elif user_id is not None and comment_id is not None:
        # Удаляем конкретный комментарий пользователя
        query = """
        DELETE FROM task_comments
        WHERE task_id = %s AND user_id = %s AND id = %s
        """
        params = (task_id, user_id, comment_id)
    elif user_id is not None:
        # Удаляем все комментарии этого пользователя
        query = """
        DELETE FROM task_comments
        WHERE task_id = %s AND user_id = %s
        """
        params = (task_id, user_id)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, params)
    conn.commit()

    cursor.close()
    conn.close()

def get_task_comments(task_id, user_id=None):
    query = """
        SELECT id, task_id, user_id, comment
        FROM task_comments
        WHERE task_id = %s
    """

    # Если указан user_id, фильтруем по нему
    if user_id:
        query += " AND user_id = %s"

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (task_id, user_id) if user_id else (task_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments

def get_task_comment(comment_id, user_id):
    query = """
        SELECT id, task_id, user_id, comment
        FROM task_comments
        WHERE id = %s AND user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (comment_id, user_id))
    comment = cursor.fetchone()

    cursor.close()
    conn.close()

    return comment
