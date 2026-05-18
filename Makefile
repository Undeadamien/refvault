SOURCES = src
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

test:
	@pytest --cov

#todo: verify xdg-open
docs:
	@xdg-open http://localhost:8000/docs

#todo: verify xdg-open
admin:
	@xdg-open http://localhost:8000/admin

.PHONY: dev up down build clean re lint test format docs admin
