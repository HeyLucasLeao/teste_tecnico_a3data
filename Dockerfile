FROM python:3.11-slim-bookworm as builder

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY . .

RUN poetry install --no-interaction --no-ansi --no-root

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "main.py"]