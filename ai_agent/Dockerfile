# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file, application code, and entrypoint script
COPY ./ai_agent/requirements.txt /app/ai_agent/
COPY ./ai_agent /app/ai_agent/
COPY ./ai_agent/entrypoint.sh /app/ai_agent/

# Set workdir for pip install
WORKDIR /app/ai_agent

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Set the entrypoint that runs migrations
ENTRYPOINT ["/app/ai_agent/entrypoint.sh"]

# Default command to run (passed to entrypoint)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
