ARG PYTHON_VERSION="3.8.6"
FROM python:${PYTHON_VERSION}-slim-buster

CMD ["python3"]

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/

# hadolint ignore=DL3013
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    netcat=1.10-41.1 \
    libpq-dev=11.9-0+deb10u1 \
    unixodbc-dev=2.3.6-0.1 \
    g++=4:8.3.0-1 \
 && pip install --no-cache-dir -U pip setuptools \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get clean
