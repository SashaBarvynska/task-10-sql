# pull official base image
FROM python:3.10.0-slim-buster

# set work directory
WORKDIR /app
COPY pyproject.toml /app/

# install dependencies
RUN pip install poetry

# helping libraries for install and run psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN poetry install

# copy tests
COPY tests /app/tests
COPY config.py /app/config.py

RUN pytest tests/
# copy project
COPY src /app/src

# start the server
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
