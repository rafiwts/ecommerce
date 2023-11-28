#!/bin/bash

# Activate the virtual environment
source /app/.venv/bin/activate

# Run migrations within the virtual environment
python /app/manage.py makemigrations

if [[ $(python /app/manage.py makemigrations --dry-run | grep 'No changes detected') ]]; then
    echo "Migrations will not be run as no changes have been detected."
else
    python /app/manage.py migrate
fi

# Start the Django development server within the virtual environment
python /app/manage.py runserver 0.0.0.0:8000
