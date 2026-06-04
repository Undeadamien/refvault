SOURCES = refvault
TESTS = tests
TARGETS = $(SOURCES) $(TESTS)

dev:
	pip install -e ".[dev]" black isort pyright

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

clean:
	docker compose down -v

re: clean
	docker compose up --build -d

lint:
	@black --check -q $(TARGETS)
	@isort --check-only -q --profile black $(TARGETS)
	@pyright $(TARGETS)

format:
	@black -q --fast $(TARGETS)
	@isort -q --profile black $(TARGETS)

migrate:
	docker compose exec app alembic upgrade head

test:
	@pytest --cov

docs:
	@xdg-open http://localhost:8000/docs

admin:
	@xdg-open http://localhost:8000/admin

.PHONY: dev up down build clean re lint test format docs admin
