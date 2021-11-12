FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN-PROJECT=true

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update -qq && apt-get install -y vim git curl libpq-dev gcc && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

RUN mkdir -p /home/django/app
ENV WORK_DIR=/home/django/app

WORKDIR $WORK_DIR
COPY pyproject.toml poetry.lock $WORK_DIR
RUN poetry export --without-hashes --dev -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000