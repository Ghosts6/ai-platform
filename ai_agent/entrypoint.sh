#!/bin/sh
set -e

cd /app/ai_agent

python manage.py collectstatic --noinput

exec "$@"
