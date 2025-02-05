# FastAPI Application Service

Микросервис для управления заявками, построенный на FastAPI с использованием PostgreSQL, Docker и Kafka.

## 🚀 Быстрый старт

### Требования

- Docker
- Docker Compose
- Python 3.11+

### Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/fastapi-app-service.git
   cd fastapi-app-service
   cp .env.example .env
   docker-compose up -d --build
   docker-compose exec web alembic upgrade head
   docker-compose exec web alembic alembic revision --autogenerate -m "migration_name"
    
2. Сервис будет доступен по адресу: http://localhost:8000/docs/

🛠 Технологии

    FastAPI - веб-фреймворк

    PostgreSQL - основная база данных

    Alembic - управление миграциями

    Kafka - обработка событий

    Docker - контейнеризация

    AsyncPG - асинхронный драйвер для PostgreSQL

📚 API Endpoints

1. Создание новой заявки
   - POST /applications/

2. Получить список заявок.
   - GET /applications/?page=1&size=10

4. Получить заявки по имени пользователя.
   - GET /applications/{user_name}?page=1&size=10

🐳 Docker Compose

Сервисы:

    web - FastAPI приложение (порт 8000)
    db - PostgreSQL (порт 5432)
    kafka - Kafka брокер (порт 9092)
    zookeeper - Zookeeper для Kafka (порт 2181)
