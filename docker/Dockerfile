FROM python:3.11-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1


WORKDIR /src

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends python3-pip && \
    apt install -y postgresql-client libpq-dev gcc && \
    apt autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml /src/pyproject.toml
COPY poetry.lock /src/poetry.lock

RUN poetry install

COPY ./src /src
