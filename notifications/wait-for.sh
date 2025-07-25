#!/bin/sh

HOST="$1"
shift

echo "Waiting for $HOST..."

while ! nc -z $(echo $HOST | cut -d: -f1) $(echo $HOST | cut -d: -f2); do
  sleep 1
  echo "Waiting for $HOST..."
done

echo "$HOST is available. Starting application."

exec "$@"
