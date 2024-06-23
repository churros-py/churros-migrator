#!/bin/bash

# Wait for the database to be available
while ! nc -z db 5432; do
  echo "Waiting for database..."
  sleep 1
done

# Run Alembic migrations
alembic upgrade head

echo "Database migration completed."
