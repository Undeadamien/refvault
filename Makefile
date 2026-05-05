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

.PHONY: up down build rebuild clean re
