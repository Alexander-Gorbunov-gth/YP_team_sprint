#!/usr/bin/env bash

set -e

POSTGRES_HOST="${SQL_HOST}"
POSTGRES_PORT="${SQL_PORT:-5432}"
ES_HOST="${ELASTIC_HOST:-elasticsearch_movies}"
ES_PORT="${ELASTIC_PORT:-9200}"

echo "⏳ Ожидаем PostgreSQL на ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL доступен"

echo "⏳ Ожидаем Elasticsearch на ${ES_HOST}:${ES_PORT}..."
until curl -s "http://${ES_HOST}:${ES_PORT}" >/dev/null; do
  sleep 1
done
echo "✅ Elasticsearch доступен"

echo "🚀 Запускаем ETL"
exec python /opt/app/main.py