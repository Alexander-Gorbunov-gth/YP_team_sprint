.PHONY: run
run:
	@docker compose -f docker-compose.override.yml build && docker compose -f docker-compose.override.yml up

.PHONY: auth
auth:
	@docker compose -f docker-compose.auth_sprint.yaml build && docker compose -f docker-compose.auth_sprint.yaml up

diplom:
	docker compose -f docker-compose.diplom.yml build && docker compose -f docker-compose.diplom.yml up

book:
	docker compose -f docker-compose.diplom.yml build  booking_service && docker compose -f docker-compose.diplom.yml up booking_service