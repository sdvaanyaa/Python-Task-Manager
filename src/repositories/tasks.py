import psycopg2
from ..settings import DB_CONFIG
def create_task(user_id, title, description, status, created_at):
    query = """
        INSERT INTO tasks (user_id, title, description, status, created_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id, title, description, status, created_at))
    conn.commit()

    task_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return task_id

def get_all_tasks():
    query = """
        SELECT id, user_id, title, description, status, created_at
        FROM tasks
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks

def get_tasks_by_uesr(user_id):
    query = """
        SELECT id, user_id, title, description, status, created_at
        FROM tasks
        WHERE user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks

def delete_task(task_id):
    delete_comments_query = """
        DELETE FROM task_comments
        WHERE task_id = %s
    """
    delete_tags_query = """
        DELETE FROM task_tags_map
        WHERE task_id = %s
    """
    delete_task_query = """
        DELETE FROM tasks
        WHERE id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(delete_tags_query, (task_id,))
    cursor.execute(delete_comments_query, (task_id,))
    cursor.execute(delete_task_query, (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

def delete_all_tasks():
    query = """
        DELETE FROM tasks
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()