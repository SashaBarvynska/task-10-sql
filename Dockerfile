# pull official base image
FROM python:3.10.5-slim-buster

ENV APP_HOST=0.0.0.0
ENV APP_PORT=5008
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=0672934823a
ENV POSTGRES_DB=postgres
ENV POSTGRES_PORT=5432
ENV DATABASE=postgresql://$POSTGRES_DB:$POSTGRES_PASSWORD@main_db:$POSTGRES_PORT/$POSTGRES_USER
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
