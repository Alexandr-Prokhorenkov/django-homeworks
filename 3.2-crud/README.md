# Stocks Products — Django REST API

REST API для управления товарами и складами на Django REST Framework.

Проект запускается в Docker-контейнере и использует SQLite вместо PostgreSQL.

## Технологии

- Python 3.10
- Django
- Django REST Framework
- SQLite
- Docker

## Структура API

Основной адрес API:

http://localhost:8000/api/v1/

Доступные endpoints:

- GET/POST /api/v1/products/
- GET/POST /api/v1/stocks/

## Требования

Для запуска проекта необходимо установить:

- Docker
- Git

PostgreSQL для запуска проекта не требуется.

## Сборка Docker image

Перейдите в корневую директорию проекта, где находится Dockerfile, и выполните:

```bash
docker build -t stocks-products .
