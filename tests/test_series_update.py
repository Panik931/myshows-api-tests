import json

import allure
import psycopg
import pytest

from utils.constants import (
    SERIES_URL,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


@allure.title("PUT /series/{series_id}: обновление поля {field}")
@allure.severity(allure.severity_level.CRITICAL)
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

    allure.attach(
        str(series_id),
        name="ID сериала для обновления",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("Формируем тело запроса с обновлённым полем"):
        payload = {
            "name": "Тестовый сериал",
            "photo": "https://example.com/old-photo.jpg",
            "rating": 8,
            "status": "watching",
            "review": "Старый отзыв",
        }
        payload[field] = value

        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False),
            name="Тело запроса PUT",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step(f"Отправляем PUT-запрос для обновления поля '{field}'"):
        response = session.put(
            f"{SERIES_URL}/{series_id}",
            json=payload,
        )

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step(f"Подключаемся к БД и проверяем, что поле '{field}' обновилось"):
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
                    f"SELECT {field} FROM series WHERE id = %s",
                    (series_id,),
                )
                result = cursor.fetchone()

            with allure.step("Проверяем, что запись найдена и значение совпадает с ожидаемым"):
                assert result is not None, "Запись не найдена в БД"
                assert result[0] == value, f"Ожидалось {value}, получено {result[0]}"

        finally:
            connection.close()