#!/usr/bin/env bash

set -o errexit
(
  cd "$(dirname "$0")/../app"

  if [[ ! -d staticfiles ]]; then python manage.py collectstatic --noinput; fi

  python manage.py wait_for_db
  python manage.py migrate
  python manage.py create_roles

  if [[ -n "${ADMIN_USERNAME}" ]] && [[ -n "${ADMIN_EMAIL}" ]] && [[ -n "${ADMIN_PASSWORD}" ]]; then
    python manage.py create_admin --noinput --username="${ADMIN_USERNAME}" --email="${ADMIN_EMAIL}" --password="${ADMIN_PASSWORD}"
  fi

  gunicorn --bind="0.0.0.0:${PORT:-8000}" --workers="${WORKERS:-1}" app.wsgi --timeout=300 &
  gunicorn_pid="$!"

  celery --app=app worker --loglevel=INFO --concurrency="${CELERY_WORKERS:-1}" &
  celery_pid="$!"

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
)
