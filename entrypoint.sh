#!/bin/bash
set -e
export PYTHONPATH=/app

if [ -n "${AWS_SSM_PREFIX:-}" ]; then
  echo "Secrets sourced from SSM prefix: $AWS_SSM_PREFIX"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

exec "$@"
