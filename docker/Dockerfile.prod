ARG PYTHON_VERSION="3.8.12-slim-buster"
FROM python:${PYTHON_VERSION}

CMD ["python3"]

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -g 61000 doccano \
  && useradd -g 61000 -l -M -s /bin/false -u 61000 doccano

COPY --chown=doccano:doccano backend/pyproject.toml backend/poetry.lock /backend/

# hadolint ignore=DL3013
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    netcat=1.* \
    libpq-dev=11.* \
    unixodbc-dev=2.* \
    g++=4:* \
    curl \
 && pip install --upgrade pip \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
 && PATH="${PATH}:$HOME/.poetry/bin" \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev --no-root \
 && poetry add psycopg2-binary \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY --chown=doccano:doccano tools/ /opt/bin/
RUN mkdir -p /backend/staticfiles \
  && mkdir -p /backend/client/dist/static \
  && mkdir -p /backend/media \
  && mkdir -p /backend/filepond-temp-uploads \
  && chown -R doccano:doccano /backend/

COPY --chown=doccano:doccano ./backend/ /backend/
RUN ls /backend
USER doccano:doccano
VOLUME /backend/staticfiles

ENTRYPOINT [ "/opt/bin/prod-django.sh" ]
