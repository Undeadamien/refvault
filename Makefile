up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker logs -f refvault-app

clean:
	docker compose down -v

re: clean
	docker compose up --build -d

.PHONY: up down build logs clean re
