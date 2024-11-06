FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install poetry alembic
ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN poetry config virtualenvs.create false \
    && poetry env use system \
    && poetry lock \
    && poetry install --no-interaction --no-ansi --no-root