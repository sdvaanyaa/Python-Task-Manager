import psycopg2
from ..settings import DB_CONFIG
def create_tag(name):
    query = """
        INSERT INTO task_tags (name, created_at)
        VALUES (%s, NOW())
        RETURNING id
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (name,))
    tag_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return tag_id

def assign_tag_to_task(task_id, tag_id):
    query = """
        INSERT INTO task_tags_map (task_id, tag_id)
        VALUES (%s, %s)
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (task_id, tag_id))
    conn.commit()
    cursor.close()
    conn.close()

def remove_tag_from_task(task_id, tag_id):
    query = """
        DELETE FROM task_tags_map
        WHERE task_id = %s AND tag_id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (task_id, tag_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_tags_for_task(task_id):
    query = """
        SELECT tt.id, tt.name
        FROM task_tags_map ttm
        JOIN task_tags tt ON ttm.tag_id = tt.id
        WHERE ttm.task_id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (task_id,))
    tags = cursor.fetchall()
    cursor.close()
    conn.close()

    # Используем set для устранения дубликатов
    unique_tags = { (t[0], t[1]) for t in tags }
    return [{"id": t[0], "name": t[1]} for t in unique_tags]

def get_tasks_by_tag(tag_id):
    query = """
        SELECT t.id, t.title, t.description, t.status, t.created_at
        FROM task_tags_map ttm
        JOIN tasks t ON ttm.task_id = t.id
        WHERE ttm.tag_id = %s
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, (tag_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {"id": t[0], "title": t[1], "description": t[2], "status": t[3], "created_at": t[4]}
        for t in tasks
    ]

def get_all_tags():
    query = """
        SELECT id, name
        FROM task_tags
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    tags = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": t[0], "name": t[1]} for t in tags]