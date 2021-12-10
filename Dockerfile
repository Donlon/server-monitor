FROM python:3.9-slim

LABEL maintainer="kirisame@mco.moe"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_PRODUCTION=True
ENV APP_DB_PATH=/data

WORKDIR /code

RUN useradd -u 1000 django && mkdir -p /home/django ${APP_DB_PATH} && chown django:django /home/django ${APP_DB_PATH}

USER django

COPY requirements.txt .

RUN pip install --no-warn-script-location --no-cache-dir --user -r requirements.txt

COPY ./src .
COPY ./docker/entrypoint.sh /

VOLUME [ "/data" ]

ENTRYPOINT ["sh", "/entrypoint.sh"]
