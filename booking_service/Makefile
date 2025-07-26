.PHONY: run
run:
	@uvicorn src.main:app --host 0.0.0.0 --port 8050 --reload

typecheck:
	mypy src/ tests/ --explicit-package-bases

format:
	ruff format src/ tests/
	ruff check src/ tests/ --fix

lint:
	ruff check src/

dev:
	docker compose -f docker-compose.dev.yml up --build