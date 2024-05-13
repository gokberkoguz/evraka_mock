# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/usr/local/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/common"

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y curl build-essential git && \
    curl -sSL https://install.python-poetry.org/ | python3 - && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-dev

# Expose the port on which your Django app will run
EXPOSE 8000

# Command to start Django server with watchdog
CMD poetry run python manage.py migrate && poetry run python manage.py runserver_plus 0.0.0.0:8000
