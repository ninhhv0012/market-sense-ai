#!/bin/bash

# Chờ Postgres khởi động
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Thực hiện lệnh được truyền vào (ví dụ: runserver hoặc celery)
exec "$@"