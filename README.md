# My Shows Rating — API Tests

> Автоматизированные API-тесты для приложения **My Shows Rating**: проверка схем ответов и обновления данных сериалов. Запуск локально и в Docker-окружении (PostgreSQL + Backend + Tests) одной командой.

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Pytest](https://img.shields.io/badge/pytest-8.3-green.svg)
![Requests](https://img.shields.io/badge/requests-2.32-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791.svg?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg?logo=docker&logoColor=white)
![Allure](https://img.shields.io/badge/allure-2.32-8DB600.svg)

## 📋 Содержание

- [О проекте](#-о-проекте)
- [Технологии](#-технологии)
- [Структура проекта](#-структура-проекта)
- [Тест-кейсы](#-тест-кейсы)
- [Установка и запуск локально](#-установка-и-запуск-локально)
- [Запуск в Docker](#-запуск-в-docker)
- [Allure-отчёт](#-allure-отчёт)
- [Переменные окружения](#-переменные-окружения)
- [Лицензия](#-лицензия)
- [Автор](#-автор)

## 🎯 О проекте

Проект демонстрирует подход к тестированию REST API:

- ✅ валидация JSON-схем ответов при разном объёме данных в БД;
- ✅ проверка обновления каждого поля сущности `series` через `PUT`;
- ✅ подготовка тестовых данных напрямую в PostgreSQL (SQL-фикстуры);
- ✅ параметризация тестов (`pytest.mark.parametrize`, indirect-фикстуры);
- ✅ подробная Allure-разметка: шаги, вложения тел запросов и ответов;
- ✅ полный запуск окружения через Docker Compose: БД → бэкенд → тесты.

## 🛠 Технологии

| Инструмент | Назначение |
|---|---|
| Python 3.14, pytest | язык и тестовый фреймворк |
| requests | HTTP-клиент |
| psycopg2-binary | работа с PostgreSQL |
| jsonschema | валидация JSON-схем |
| allure-pytest | отчётность |
| Docker / Docker Compose | контейнеризация и оркестрация окружения |

## 📁 Структура проекта

```text
myshows_api_tests/
├── tests/                  # тесты
│   ├── test_series.py      # GET /series: валидация JSON-схемы
│   └── test_series_update.py # PUT /series/{id}: обновление полей
├── utils/
│   ├── api_client.py       # HTTP-клиент (requests.Session)
│   ├── constants.py        # URL и параметры БД (через os.getenv)
│   └── db.py               # подключение к PostgreSQL
├── data/                   # SQL-фикстуры с тестовыми данными
├── schemas/                # JSON-схемы ответов API
├── conftest.py             # фикстуры (session, series_data, series_to_update)
├── pytest.ini              # конфигурация pytest
├── requirements.txt        # зависимости Python
├── dockerfile              # образ тестов
├── docker-compose.yml      # msr-db + msr-backend + api-tests
├── .env.example            # пример переменных окружения
└── README.md