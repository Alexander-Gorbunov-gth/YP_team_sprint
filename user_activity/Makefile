run:
	uvicorn src.main:app

reload:
	uvicorn src.main:app --reload

sort:
	isort --line-length 120 .

format:
	black --line-length 120 .

check:
	flake8 .