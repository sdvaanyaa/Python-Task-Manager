import bcrypt
import psycopg2
from ..settings import DB_CONFIG
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def authenticate_user(username, password):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT id ,username, password, role_id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        user_id, username, stored_password, role_id = row

        if verify_password(password, stored_password):
            return {
                "user_id": user_id,
                "authenticated": True,
                "username": username,
                "role_id": role_id
            }
        else:
            return {"authenticated": False, "message": "Неверный пароль"}
    else:
        return {"authenticated": False, "message": "Пользователь не найден"}
