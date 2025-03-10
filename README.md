# FastAPI Application Service DDD

An example microservice built on FastAPI using PostgresSQL, Docker and Kafka.

## 🚀 Quick start

### Requirements

- Docker
- Docker Compose
- Kafka
- Make utils (Does not support Windows)
- Python 3.11+

### Installation and launch

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/fastAPI-kafka-example.git
   cd fastAPI-kafka-example
   cp .env.example .env
   docker-compose up -d --build
   docker-compose exec web alembic upgrade head
   docker-compose exec web alembic alembic revision --autogenerate -m "migration_name"
    
2. Web service will be : http://localhost:8000/docs/

🛠 Techs

    FastAPI - web framework

    PostgreSQL - main database 

    Alembic - magration service

    Kafka - event processing

    Docker - containerization

    AsyncPG - async drivere for PostgreSQL

🐳 Docker Compose

Service:

    web - FastAPI app (port 8000)
    db - PostgreSQL (port 5432)
    kafka - Kafka broker (port 9092)
    zookeeper - Zookeeper for Kafka (port 2181)


Additional docs:

- https://docs.python.org/3/howto/logging.html Python logger
- https://docs.pydantic.dev/latest/ Pydantic
- https://fastapi-users.github.io/fastapi-users/latest/ FastAPI users
- https://docs.python.org/3/library/asyncio.html asyncio python