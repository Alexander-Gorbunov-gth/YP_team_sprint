#!/bin/bash

echo "Контейнер стартует"

echo "Жду подключения к Redis..."
python3 /app/tests/functional/utils/wait_for_redis.py
echo "Redis успешно запущен!"

echo "-------Запуск тестов-------"
pytest -v
