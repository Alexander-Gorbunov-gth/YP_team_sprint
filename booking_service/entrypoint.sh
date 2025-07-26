#!/bin/bash

echo "Ожидание PostgreSQL..."
echo данные - $POSTGRES_HOST $POSTGRES_PORT
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 5
done
echo "PostgreSQL готов!"

echo "Применение миграций Alembic..."
alembic upgrade head

python -m uvicorn src.main:app --host 0.0.0.0 --port 8050