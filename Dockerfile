FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "creyp.wsgi"]