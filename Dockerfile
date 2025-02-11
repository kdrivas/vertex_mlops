FROM python:3.11.11-slim

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH

WORKDIR /app

# Install dependencies
COPY pyproject.toml pyproject.toml
COPY price_model price_model
RUN poetry install --only-root
