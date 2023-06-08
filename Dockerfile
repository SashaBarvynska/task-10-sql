# pull official base image
FROM python:3.10.5-slim-buster

# set work director
WORKDIR /app
# helping libraries for install and run psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
# install dependencies
COPY pyproject.toml /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . /app/
