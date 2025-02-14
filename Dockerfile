FROM python:3.11.11-slim

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY pyproject.toml pyproject.toml
COPY price_model price_model
RUN poetry install

ENV PATH="/app/.venv/bin:$PATH"