#!/usr/bin/env bash

set -o errexit

echo "Making staticfiles"
if [[ ! -d "app/staticfiles" ]]; then python app/manage.py collectstatic --noinput; fi

echo "Initializing database"
python app/manage.py wait_for_db
python app/manage.py migrate
python app/manage.py create_roles

echo "Creating admin"
if [[ -n "${ADMIN_USERNAME}" ]] && [[ -n "${ADMIN_PASSWORD}" ]] && [[ -n "${ADMIN_EMAIL}" ]]; then
  python app/manage.py create_admin \
    --username "${ADMIN_USERNAME}" \
    --password "${ADMIN_PASSWORD}" \
    --email "${ADMIN_EMAIL}" \
    --noinput \
  || true
fi

echo "Starting django"
gunicorn --bind="0.0.0.0:${PORT:-8000}" --workers="${WORKERS:-1}" --pythonpath=app app.wsgi --timeout 300
