.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  up                - Run app locallu with uv and uvicorn"
	@echo "  up -d             - Run app in background with uv and uvicorn"
	@echo "  down              - Stop all containers (docker-compose down)"
	@echo "  restart           - Restart all containers (down + up)"
	@echo "  test              - Run container with tests (docker-compose-test.yaml)"
	@echo "  migrate-create    - Create new migration with Alemibc inside container (MIGRATION='msg')"
	@echo "  migrate-apply     - Apply migrations inside container"
	@echo "  run locally       - Run all containers locally (docker-compose up --build)"

run locally:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

migrate-create:
	docker-compose exec web alembic revision --autogenerate -m "$(MIGRATION)"

migrate-apply:
	docker-compose exec web alembic upgrade head

build-background:
	docker-compose up -d

build:
	docker-compose up --build

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up --build

test:
	docker-compose -f docker-compose-test.yaml up --build --abort-on-container-exit
	docker-compose -f docker-compose-test.yaml down
