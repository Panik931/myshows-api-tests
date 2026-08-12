import psycopg

from utils.constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_db_connection():
    return psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="my-shows-rating",
        user="postgres",
        password="123456",
    )