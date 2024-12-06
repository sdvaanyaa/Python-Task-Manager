import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Примеры хэширования
passwords = {
    "superadmin": hash_password("superadmin"),
    "admin_mark": hash_password("admin_mark"),
    "john_doe": hash_password("john_doe"),
    "user_smith": hash_password("user_smith"),
    "guest_user": hash_password("guest_user"),
    "nikita_ponomarev": hash_password("nikita_ponomarev")
}

# Выводим хэши для использования в SQL
for username, hashed_password in passwords.items():
    print(f"{hashed_password}")