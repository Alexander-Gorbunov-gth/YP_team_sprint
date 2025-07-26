FROM python:3.12
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./pyproject.toml .

RUN apt update && apt install -y netcat-openbsd
RUN pip install --upgrade pip \
     && pip install --no-cache-dir poetry==1.7.1 \
     && poetry config virtualenvs.create false \
     && poetry install --no-interaction --no-ansi --no-root

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8050"]
