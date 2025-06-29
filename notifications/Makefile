.PHONY: run_docker
run_docker:
	@docker compose -f docker-compose.gorbunov.yml build && docker compose -f docker-compose.gorbunov.yml up

.PHONY: auth
auth:
	@docker compose -f docker-compose.auth_sprint.yaml build && docker compose -f docker-compose.auth_sprint.yaml up

.PHONY: run
run:
	@uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

sort:
	isort --line-length 120 .

format:
	black --line-length 120 .

check:
	flake8 --max-line-length 120 src/
