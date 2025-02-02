.DEFAULT_GOAL := help

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head