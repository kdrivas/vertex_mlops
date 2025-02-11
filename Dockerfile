FROM python:3.11.11-slim

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Install dependencies
COPY pyproject.toml pyproject.toml
COPY price_model price_model
RUN poetry install --only-root
