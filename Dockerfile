# pull official base image
FROM python:3.10.0-slim-buster

# set work directory
WORKDIR /app
# helping libraries for install and run psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="/root/.poetry/bin:${PATH}"    

# install dependencies
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-dev

COPY . /app/

# start the server
ENTRYPOINT ["python", "main.py"]
