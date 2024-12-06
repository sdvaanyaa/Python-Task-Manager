import os
from dotenv import load_dotenv

load_dotenv(".env")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

POOL_MIN_CONN = int(os.getenv("POOL_MIN_CONN", 1))
POOL_MAX_CONN = int(os.getenv("POOL_MAX_CONN", 10))