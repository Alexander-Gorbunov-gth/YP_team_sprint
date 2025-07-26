#!/bin/bash

echo "Ожидание PostgreSQL..."
echo данные - $POSTGRES_HOST $POSTGRES_PORT
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 5
done
echo "PostgreSQL готов!"

echo "Применение миграций Alembic..."
alembic upgrade head
