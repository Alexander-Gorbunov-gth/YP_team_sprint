#!/bin/bash

echo "Ожидание PostgreSQL..."
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 1
done
echo "PostgreSQL готов!"

echo "Ожидание Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 1
done
echo "Redis готов!"

echo "Применение миграций Alembic..."
alembic upgrade head

echo "Запуск приложения..."
exec "$@"
