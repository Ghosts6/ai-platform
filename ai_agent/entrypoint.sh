#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check and seed the knowledge base if it's empty
echo "Checking knowledge base..."
python manage.py check_and_seed

# Start server
echo "Starting server..."
exec "$@"
