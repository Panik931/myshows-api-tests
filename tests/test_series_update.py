import pytest
import psycopg

from utils.constants import (
    SERIES_URL,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "Новое название"),
        ("photo", "https://example.com/new-photo.jpg"),
        ("rating", 10),
        ("status", "watched"),
        ("review", "Новый отзыв"),
    ],
)
def test_update_series_field(session, series_to_update, field, value):

    series_id = series_to_update

    # Полное тело запроса.
    payload = {
        "name": "Тестовый сериал",
        "photo": "https://example.com/old-photo.jpg",
        "rating": 8,
        "status": "watching",
        "review": "Старый отзыв",
    }

    # Меняем только проверяемое поле
    payload[field] = value

    response = session.put(
        f"{SERIES_URL}/{series_id}",
        json=payload,
    )

    print("URL:", response.url)
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 200

    # Проверяем изменение непосредственно в БД
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
                f"""
                SELECT {field}
                FROM series
                WHERE id = %s
                """,
                (series_id,),
            )

            result = cursor.fetchone()

        assert result is not None
        assert result[0] == value

    finally:
        connection.close()