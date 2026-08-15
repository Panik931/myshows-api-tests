import json
import time

import allure
import requests


class ApiClient:
    """
    Обёртка над requests:
    - логирует каждый вызов в allure (URL, заголовки, тела, статус-код);
    - автоматически повторяет запрос при 429 (rate limit).
    """

    def __init__(self, base_url="", session=None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    # --- HTTP-методы ---------------------------------------------------
    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def request(self, method, path, max_retries=5, retry_delay=3, **kwargs):
        # Поддерживает и относительные пути, и полные URL
        url = path if path.startswith("http") else f"{self.base_url}{path}"

        with allure.step(f"{method} {path}"):
            response = self._request_with_retry(
                method, url, max_retries, retry_delay, **kwargs
            )
            self._log_to_allure(url, response)
            return response

    # --- Повторы при rate limit (429) ----------------------------------
    def _request_with_retry(self, method, url, max_retries, retry_delay, **kwargs):
        for attempt in range(max_retries):
            response = self.session.request(method, url, **kwargs)

            if response.status_code != 429:
                return response

            with allure.step(
                f"429 Too Many Requests: пауза {retry_delay} c, "
                f"повтор {attempt + 1}/{max_retries}"
            ):
                time.sleep(retry_delay)

        return response

    # --- Логирование вызова в allure ------------------------------------
    @staticmethod
    def _log_to_allure(url, response):
        request = response.request

        allure.attach(
            f"{request.method} {url}",
            name="URL запроса",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            json.dumps(dict(request.headers), indent=2, ensure_ascii=False),
            name="Заголовки запроса",
            attachment_type=allure.attachment_type.JSON,
        )
        if request.body:
            body = request.body
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            allure.attach(
                body, name="Тело запроса",
                attachment_type=allure.attachment_type.JSON,
            )

        allure.attach(
            str(response.status_code),
            name="Код ответа",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            json.dumps(dict(response.headers), indent=2, ensure_ascii=False),
            name="Заголовки ответа",
            attachment_type=allure.attachment_type.JSON,
        )
        try:
            response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        except ValueError:
            response_body = response.text
        allure.attach(
            response_body, name="Тело ответа",
            attachment_type=allure.attachment_type.JSON,
        )