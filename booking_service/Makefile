.PHONY: run
run:
	@uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

typecheck:
	mypy src/ tests/ --explicit-package-bases

format:
	ruff format src/ tests/
	ruff check src/ tests/ --fix

lint:
	ruff check src/

format-path:
	ruff format $(PATH)
	ruff check $(PATH) --fix

lint-path:
	ruff check $(PATH)

typecheck-path:
	mypy $(PATH) --explicit-package-bases

	