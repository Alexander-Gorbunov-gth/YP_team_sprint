run:
	python3 -m src.main

typecheck:
	mypy src/ tests/ --explicit-package-bases

format:
	ruff format src/ tests/
	ruff check src/ tests/ --fix

lint:
	ruff check src/
	