#!/usr/bin/env bash

set -o errexit

if [[ ! -d "app/staticfiles" ]]; then python3 app/manage.py collectstatic --noinput; fi

python3 app/manage.py wait_for_db
python3 app/manage.py migrate

if [[ -n "${ADMIN_USERNAME}" ]] && [[ -n "${ADMIN_EMAIL}" ]] && [[ -n "${ADMIN_PASSWORD}" ]]; then
  python3 app/manage.py create_admin --noinput --username="${ADMIN_USERNAME}" --email="${ADMIN_EMAIL}" --password="${ADMIN_PASSWORD}"
fi

gunicorn --bind="0.0.0.0:${PORT:-8000}" --workers="${WORKERS:-1}" --pythonpath=app app.wsgi --timeout 300
