#!/usr/bin/env bash

set -o errexit

echo "Making staticfiles"
static_dir=staticfiles
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
gunicorn --bind="0.0.0.0:${PORT:-8000}" --workers="${WORKERS:-1}" app.wsgi --timeout 300

