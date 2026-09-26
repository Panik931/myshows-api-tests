import os

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1/api/v1")

SERIES_URL = f"{BASE_URL}/series"

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = 5432
DB_NAME = "my-shows-rating"
DB_USER = "postgres"
DB_PASSWORD = "123456"