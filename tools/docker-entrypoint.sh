#!/usr/bin/env bash
set -o errexit

if [[ -z "${VIRTUAL_ENV}" ]]; then
    source "$(pipenv --venv)/bin/activate"
fi

#root="$(dirname "$0")/.."
#app="${root}/app"
app="/src/app"

echo "Initializing database"
python "${app}/manage.py" wait_for_db
python "${app}/manage.py" migrate
python "${app}/manage.py" create_roles

if [[ -n "${ADMIN_USERNAME}" ]] && [[ -n "${ADMIN_PASSWORD}" ]] && [[ -n "${ADMIN_EMAIL}" ]]; then
  python "${app}/manage.py" create_admin \
    --username "${ADMIN_USERNAME}" \
    --password "${ADMIN_PASSWORD}" \
    --email "${ADMIN_EMAIL}" \
    --noinput \
  || true
fi

echo "Starting django"
python -u "${app}/manage.py" runserver 0.0.0.0:8000
