import bcrypt
import psycopg2
from ..settings import DB_CONFIG

def create_user(role_id, username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = """
        INSERT INTO users (role_id, username, email, password, created_at)
        VALUES (%s, %s, %s, %s, NOW())
        RETURNING id
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (role_id, username, email, hashed_password))
    conn.commit()

    user_id = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return user_id

def get_user(user_id):
    query = """
        SELECT id, role_id, username, email, created_at
        FROM users
        WHERE id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_username_by_id(user_id):
    query = """
        SELECT username
        FROM users
        WHERE id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None


def get_all_users():
    query = """
        SELECT id, username FROM users
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Преобразуем кортежи в словари
    return [{"id": user[0], "username": user[1]} for user in users]