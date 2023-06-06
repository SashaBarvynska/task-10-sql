# pull official base image
FROM python:3.10.5-slim-buster
ENV APP_HOST=0.0.0.0
ENV APP_PORT=5008
ENV DATABASE=postgresql://postgres:0672934823a@main_db:5432/postgres
ENV TEST_DATABASE=postgresql://postgres:0672934823a@main_db:5432/test_db
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
