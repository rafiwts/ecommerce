#!/bin/bash

# Wait for the database to be ready
python /app/ecommerce/wait_for_db.py

# Apply database migrations
python manage.py migrate

# Run the development server
python manage.py runserver 0.0.0.0:8000

# Run the development server
exec "$@"
