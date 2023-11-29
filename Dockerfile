FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install poetry and poetry files
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install --no-root

# install pip and generate requirements.txt from poetry
RUN pip install --upgrade pip
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
