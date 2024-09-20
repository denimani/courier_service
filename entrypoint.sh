#!/bin/sh

timeout=60
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
  timeout=$((timeout - 1))
  if [ $timeout -le 0 ]; then
    echo "Не удалось дождаться готовности базы данных"
    exit 1
  fi
done

python manage.py migrate

exec "$@"
