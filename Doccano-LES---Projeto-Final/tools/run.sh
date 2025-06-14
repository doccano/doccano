#!/usr/bin/env bash

set -o errexit

if [[ -z "${ADMIN_USERNAME}" ]]; then echo "Missing ADMIN_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_PASSWORD}" ]]; then echo "Missing ADMIN_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_EMAIL}" ]]; then echo "Missing ADMIN_EMAIL environment variable" >&2; exit 1; fi
if [[ -z "${PORT}" ]]; then echo "Missing PORT environment variable" >&2; exit 1; fi
if [[ -z "${WORKERS}" ]]; then echo "Missing WORKERS environment variable" >&2; exit 1; fi
if [[ -z "${CELERY_WORKERS}" ]]; then echo "Missing CELERY_WORKERS environment variable" >&2; exit 1; fi

set -o nounset

echo "Making staticfiles"
static_dir=staticfiles
mkdir -p client/dist/static
if [[ ! -d $static_dir ]] || [[ -z $(ls -A $static_dir) ]]; then
  echo "Executing collectstatic"
  python manage.py collectstatic --noinput;
fi

echo "Initializing database"
python manage.py wait_for_db
python manage.py migrate
python manage.py create_roles

echo "Creating admin"
if [[ -n "${ADMIN_USERNAME}" ]] && [[ -n "${ADMIN_PASSWORD}" ]] && [[ -n "${ADMIN_EMAIL}" ]]; then
  python manage.py create_admin \
    --username "${ADMIN_USERNAME}" \
    --password "${ADMIN_PASSWORD}" \
    --email "${ADMIN_EMAIL}" \
    --noinput \
  || true
fi

echo "Starting django"
gunicorn \
  --bind="0.0.0.0:${PORT:-8000}" \
  --workers="${WORKERS:-1}" \
  --timeout=300 \
  --capture-output \
  --log-level info \
  config.wsgi &
gunicorn_pid="$!"

echo "Starting celery"
celery --app=config worker --loglevel=INFO --concurrency="${CELERY_WORKERS:-1}" &
celery_pid="$!"

echo "Starting flower"
if [[ -n "${FLOWER_BASIC_AUTH:-}" ]]; then
  celery --app=config flower --basic_auth="${FLOWER_BASIC_AUTH}" &
fi

while :; do
  if [[ ! -e "/proc/${celery_pid}" ]]; then
    echo "celery crashed" >&2
    exit 1
  elif [[ ! -e "/proc/${gunicorn_pid}" ]]; then
    echo "gunicorn crashed" >&2
    exit 2
  else
    sleep 10
  fi
done
