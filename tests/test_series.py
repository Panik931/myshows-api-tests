from utils.constants import SERIES_URL


def test_get_series(session, series_data):
    response = session.get(SERIES_URL)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == len(series_data)

    for expected in series_data:
        actual = next(
            item for item in data
            if item["id"] == expected["id"]
        )

        assert actual["name"] == expected["name"]
        assert actual["photo"] == expected["photo"]
        assert actual["rating"] == expected["rating"]
        assert actual["status"] == expected["status"]
        assert actual["review"] == expected["review"]