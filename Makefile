.PHONY: up down logs api worker test lint fmt
up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

api:
	docker compose up --build api

worker:
	docker compose up --build worker

test:
	docker compose run --rm api sh -lc "uv run pytest -q"

lint:
	docker compose run --rm api sh -lc "uv run ruff check ."
	
fmt:
	docker compose run --rm api sh -lc "uv run ruff format ."
