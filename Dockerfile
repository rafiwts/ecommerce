# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client

# Copy the poetry files and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install --no-root

# Copy the entire project to the working directory
COPY . /app/

# Run Django migrations
RUN poetry run python manage.py makemigrations

# Other necessary commands for your Dockerfile
# ...

# Specify the command to run on container start
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
