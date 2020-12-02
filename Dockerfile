ARG PYTHON_VERSION="3.8.6"
ARG NODE_VERSION="13.7"
FROM node:${NODE_VERSION}-alpine AS frontend-builder

COPY frontend/ /frontend/
WORKDIR /frontend
ENV PUBLIC_PATH="/static/_nuxt/"

# hadolint ignore=DL3018
RUN apk add -U --no-cache git python3 make g++ \
 && yarn install \
 && yarn build \
 && apk del --no-cache git make g++

FROM python:${PYTHON_VERSION}-slim-buster AS backend-builder

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    netcat=1.10-41.1 \
    libpq-dev=11.9-0+deb10u1 \
    unixodbc-dev=2.3.6-0.1 \
    g++=4:8.3.0-1 \
 && apt-get clean

COPY /app/requirements.txt /
# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -r /requirements.txt \
 && pip wheel --no-cache-dir -r /requirements.txt -w /deps

FROM python:${PYTHON_VERSION}-slim-buster AS runtime

RUN useradd -ms /bin/sh doccano

RUN mkdir /data \
 && chown doccano:doccano /data

COPY --from=backend-builder /deps /deps
# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir /deps/*.whl

COPY --chown=doccano:doccano . /doccano
WORKDIR /doccano
COPY --from=frontend-builder /frontend/dist /doccano/app/client/dist
RUN python app/manage.py collectstatic --noinput

VOLUME /data
ENV DATABASE_URL="sqlite:////data/doccano.db"

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="8000"
ENV WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

USER doccano
WORKDIR /doccano
EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
