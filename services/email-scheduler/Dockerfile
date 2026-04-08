FROM python:3.13-alpine AS builder

RUN apk add --no-cache gcc musl-dev postgresql-dev libffi-dev

RUN pip install --no-cache-dir poetry==2.0.1

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

FROM python:3.13-alpine

RUN apk add --no-cache libpq curl

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .