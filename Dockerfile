FROM python:3.10.7-slim-bullseye

WORKDIR app/
RUN apt-get update && \
      apt-get -y install libpq-dev python3-dev gcc default-jre

COPY . /app

RUN pip3 install --upgrade "pip>=22.1"
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
RUN pip3 install psycopg2-binary --no-binary psycopg2-binary
RUN pip3 install dbt-postgres