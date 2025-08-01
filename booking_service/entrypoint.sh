#!/bin/bash

echo "Ожидание PostgreSQL..."
echo данные - $POSTGRES_HOST $POSTGRES_PORT
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 5
done
echo "PostgreSQL готов!"

echo "Применение миграций Alembic..."
alembic upgrade head

exec gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8050 \
  --timeout 120