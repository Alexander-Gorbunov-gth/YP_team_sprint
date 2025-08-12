#!/bin/bash

echo "Ожидание PostgreSQL..."
echo данные - $POSTGRES_HOST $POSTGRES_PORT
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 5
done

echo "PostgreSQL готов!"

echo "Ожидание RabbitMQ..."

while ! nc -z $(echo $RABBITMQ_HOST | cut -d: -f1) $(echo $RABBITMQ_PORT | cut -d: -f2); do
  sleep 1
  echo "Waiting for $RABBITMQ_HOST..."
done

echo "Применение миграций Alembic..."
alembic upgrade head

# exec gunicorn src.main:app \
#   --workers 4 \
#   --worker-class uvicorn.workers.UvicornWorker \
#   --bind 0.0.0.0:8050 \
#   --timeout 120
python -m uvicorn src.main:app --host 0.0.0.0 --port 8050 --reload