import pytest
import psycopg
import requests

from utils.constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


@pytest.fixture(scope="session")
def session():
    session = requests.Session()

    yield session

    session.close()


@pytest.fixture
def series_data():
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    try:
        with connection.cursor() as cursor:

            # Очищаем таблицу перед тестом
            cursor.execute("DELETE FROM series")

            # Добавляем тестовые данные
            cursor.execute(
                """
                INSERT INTO series
                    (name, photo, rating, status, review)
                VALUES
                    (%s, %s, %s, %s, %s),
                    (%s, %s, %s, %s, %s)
                RETURNING id, name, photo, rating, status, review
                """,
                (
                    "Тестовый сериал 1",
                    "https://example.com/series1.jpg",
                    9,
                    "watching",
                    "Отличный сериал",

                    "Тестовый сериал 2",
                    "https://example.com/series2.jpg",
                    8,
                    "watched",
                    "Хороший сериал",
                ),
            )

            rows = cursor.fetchall()

        connection.commit()

        expected_data = [
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

        yield expected_data

    finally:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM series")

        connection.commit()
        connection.close()