#!/bin/sh
set -e

cd /app/ai_agent

python manage.py collectstatic --noinput

python manage.py index_documents data

exec "$@"
