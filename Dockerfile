# pull official base image
FROM python:3.10.0-slim-buster

# set work directory
WORKDIR /task-10-sql

# install dependencies
RUN pip install poetry
COPY ./pyproject.toml /task-10-sql/pyproject.toml
RUN poetry install

# copy project
COPY . /task-10-sql
# expose port
EXPOSE 5000
# start the server
CMD ["flask", "run", "--host=0.0.0.0"]