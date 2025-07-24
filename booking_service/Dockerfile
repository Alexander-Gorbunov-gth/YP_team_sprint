FROM python:3.12
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY pyproject.toml README.md ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry lock

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8050"]
