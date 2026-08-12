from utils.constants import SERIES_URL
from pathlib import Path

import pytest
import yaml
from jsonschema import validate


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
    response = session.get(SERIES_URL)
    assert response.status_code == 200

    data = response.json()

    assert len(data) == series_data

    # Загружаем JSON Schema
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "series_schema.yaml"
    )

    with open(schema_path, encoding="utf-8") as file:
        schema = yaml.safe_load(file)

    # Проверяем JSON Schema
    validate(instance=data, schema=schema)