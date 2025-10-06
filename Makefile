build:
	docker compose build

up:
	docker compose up

test:
	docker compose run --rm backend pytest

sh:
	docker compose run --rm backend bash

format:
	docker compose run --rm backend bash -c "ruff check --config ruff.toml . --fix"

check:
	docker compose run --rm backend bash -c "ruff check --config ruff.toml ."