import psycopg2
from ..settings import DB_CONFIG
def create_follow(following_user_id, followed_user_id):
    query = """
        INSERT INTO follows (following_user_id, followed_user_id, created_at)
        VALUES (%s, %s, NOW())
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (following_user_id, followed_user_id))
    conn.commit()

    cursor.close()
    conn.close()

def delete_follow(following_user_id, followed_user_id):
    query = """
        DELETE FROM follows 
        WHERE following_user_id = %s AND followed_user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (following_user_id, followed_user_id))
    conn.commit()

    cursor.close()
    conn.close()

def get_followers(user_id):
    query = """
        SELECT DISTINCT u.id, u.username
        FROM follows f
        JOIN users u ON f.following_user_id = u.id
        WHERE f.followed_user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    followers = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": follower[0], "username": follower[1]} for follower in followers]

def get_followed(user_id):
    query = """
        SELECT DISTINCT u.id, u.username
        FROM follows f
        JOIN users u ON f.followed_user_id = u.id
        WHERE f.following_user_id = %s
    """

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    followed = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": user[0], "username": user[1]} for user in followed]
