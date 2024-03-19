FROM python:3.11-alpine

RUN apk add --no-cache bash

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel pipenv
ENV WORKON_HOME /venv

COPY Pipfile* /app/
WORKDIR /app

RUN pipenv sync
COPY . /app/
WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["pipenv", "run"]
CMD ["gunicorn", "--workers", "3", "--timeout", "360", "--bind", "0.0.0.0:8000", "proxy.wsgi"]
