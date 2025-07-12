#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Build the React application
# The --prefix flag tells npm where to find the package.json
echo "Building React app..."
npm run build --prefix frontend

# Start Django development server in the background
echo "Starting Django server..."
python3 ai_agent/manage.py runserver &

# Start React development server
echo "Starting React server..."
npm start --prefix frontend
