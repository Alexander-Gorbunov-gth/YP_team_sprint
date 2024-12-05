.PHONY: run
run:
	@docker compose -f docker-compose.tests.yaml build && docker compose -f docker-compose.tests.yaml up

.PHONY: auth
auth:
	@docker compose -f docker-compose.auth_sprint.yaml build && docker compose -f docker-compose.auth_sprint.yaml up
