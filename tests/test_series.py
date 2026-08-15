from pathlib import Path

import allure
import pytest
import yaml
from jsonschema import validate

from utils.constants import SERIES_URL


@allure.title("GET /series: проверка JSON-схемы ответа при разном объёме данных")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "series_data",
    [
        None,
        "series_1.sql",
        "series_3.sql",
    ],
    indirect=True,
)
def test_get_series_schema_validation(session, series_data):
    """Проверка схемы ответа API при разном количестве данных."""

    with allure.step("Отправляем GET-запрос на получение списка сериалов"):
        response = session.get(SERIES_URL)

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    data = response.json()

    with allure.step("Проверяем, что количество сериалов совпадает с загруженным в БД"):
        assert len(data) == series_data

    with allure.step("Загружаем JSON-схему для валидации ответа"):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "series_schema.yaml"
        )
        with open(schema_path, encoding="utf-8") as file:
            schema = yaml.safe_load(file)

    with allure.step("Валидируем ответ по JSON-схеме"):
        validate(instance=data, schema=schema)