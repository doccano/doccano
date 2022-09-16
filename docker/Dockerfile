ARG PYTHON_VERSION="3.8.13-slim-bullseye"
ARG NODE_VERSION="16.16-bullseye-slim"
FROM node:${NODE_VERSION} AS frontend-builder

COPY frontend/ /frontend/
WORKDIR /frontend
ENV PUBLIC_PATH="/static/_nuxt/"
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3 make g++ ca-certificates \
 && git config --global url."https://github.com/".insteadOf git://github.com/ \
 && yarn install --network-timeout 1000000 \
 && yarn build \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

FROM python:${PYTHON_VERSION} AS backend-builder

# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    netcat=1.* \
    libpq-dev=13.* \
    unixodbc-dev=2.* \
    g++=4:* \
    libssl-dev=1.* \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
COPY backend/pyproject.toml backend/poetry.lock /tmp/
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN pip install -U --no-cache-dir pip==22.2.2 \
 && curl -sSL https://install.python-poetry.org | python - \
 && export PATH="/root/.local/bin:$PATH" \
 && poetry export --without-hashes -o /requirements.txt \
 && echo "psycopg2-binary==2.8.6" >> /requirements.txt \
 && echo "django-heroku==0.3.1" >> /requirements.txt \
 && pip install --no-cache-dir -r /requirements.txt

FROM python:${PYTHON_VERSION} AS runtime

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libpq-dev=13.* \
    unixodbc-dev=2.* \
    libssl-dev=1.* \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/sh doccano
RUN mkdir /data \
 && chown doccano:doccano /data

COPY --from=backend-builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=backend-builder /usr/local/bin/celery /usr/local/bin/celery
COPY --from=backend-builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY --chown=doccano:doccano . /doccano
WORKDIR /doccano/backend
COPY --from=frontend-builder /frontend/dist /doccano/backend/client/dist
RUN python manage.py collectstatic --noinput \
 && chown -R doccano:doccano .

VOLUME /data
ENV DATABASE_URL="sqlite:////data/doccano.db"

ENV DEBUG="False"
ENV STANDALONE="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="8000"
ENV WORKERS="2"
ENV CELERY_WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV DJANGO_SETTINGS_MODULE="config.settings.production"

USER doccano
EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
