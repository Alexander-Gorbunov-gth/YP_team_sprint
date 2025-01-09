.PHONY: run
run:
	@docker compose -f docker-compose.tests.yaml build && docker compose -f docker-compose.tests.yaml up

.PHONY: auth
auth:
	@docker compose -f docker-compose.auth_sprint.yaml build && docker compose -f docker-compose.auth_sprint.yaml up

.PHONY: auth_test
auth_test:
	@docker compose -f docker-compose.auth_test.yaml --build && docker compose -f docker-compose.auth_sprint.yaml up
