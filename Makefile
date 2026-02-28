COMPOSE_FILE=docker/docker-compose.yml

.PHONY: up down migrate migrate-init migrate-make

up:
	docker compose -f $(COMPOSE_FILE) up --build -d

down:
	docker compose -f $(COMPOSE_FILE) down

migrate-init:
	docker compose -f $(COMPOSE_FILE) run --rm app flask db init

migrate-make:
	# create a new migration (use MIGRATION_MESSAGE="..." env var)
	MIGRATION_MESSAGE?="auto"
	docker compose -f $(COMPOSE_FILE) run --rm -e MIGRATION_MESSAGE="$(MIGRATION_MESSAGE)" app flask db migrate -m "$(MIGRATION_MESSAGE)"

migrate:
	docker compose -f $(COMPOSE_FILE) run --rm app flask db upgrade
