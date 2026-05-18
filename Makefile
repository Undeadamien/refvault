SOURCES = src
TESTS = tests
TARGETS = $(SOURCES) $(TESTS)

install:
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

test:
	@pytest --cov

docs:
	@xdg-open http://localhost:8000/docs

admin:
	@xdg-open http://localhost:8000/admin

.PHONY: install up down build logs clean re lint test format docs
