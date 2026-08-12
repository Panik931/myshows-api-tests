import pytest
import psycopg
import requests

from pathlib import Path

from utils.constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


@pytest.fixture
def session():
    """Создаёт сессию requests для отправки HTTP-запросов."""
    with requests.Session() as session:
        yield session


@pytest.fixture
def series_data(request):
    """Загружает SQL-файл в БД и возвращает количество записей (для проверки схемы)."""
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        with connection.cursor() as cursor:
            # Перед тестом очищаем таблицу
            cursor.execute("DELETE FROM series")

            sql_file = getattr(request, "param", None)

            if sql_file is None:
                connection.commit()
                yield 0
                return

            file_path = (
                Path(__file__).resolve().parent
                / "data"
                / sql_file
            )

            sql = file_path.read_text(encoding="utf-8")
            cursor.execute(sql)

            # Считаем количество записей
            cursor.execute("SELECT COUNT(*) FROM series")
            count = cursor.fetchone()[0]

            connection.commit()
            yield count

    finally:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM series")
        connection.commit()
        connection.close()


@pytest.fixture
def series_list(request):
    """Загружает SQL-файл в БД и возвращает список словарей (для проверки полей)."""
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM series")

            sql_file = getattr(request, "param", None)

            if sql_file is None:
                connection.commit()
                yield []
                return

            file_path = (
                Path(__file__).resolve().parent
                / "data"
                / sql_file
            )

            sql = file_path.read_text(encoding="utf-8")
            cursor.execute(sql)

            cursor.execute(
                "SELECT id, name, photo, rating, status, review FROM series"
            )
            rows = cursor.fetchall()

            yield [
                {
                    "id": row[0],
                    "name": row[1],
                    "photo": row[2],
                    "rating": row[3],
                    "status": row[4],
                    "review": row[5],
                }
                for row in rows
            ]

    finally:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM series")
        connection.commit()
        connection.close()


@pytest.fixture
def series_to_update():
    """Создаёт сериал в БД для тестов на обновление."""
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO series
                    (name, photo, rating, status, review)
                VALUES
                    (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    "Сериал для обновления",
                    "https://example.com/original.jpg",
                    5,
                    "watching",
                    "Исходный отзыв",
                ),
            )
            series_id = cursor.fetchone()[0]

        connection.commit()
        yield series_id

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM series WHERE id = %s",
                (series_id,),
            )
        connection.commit()
        connection.close()