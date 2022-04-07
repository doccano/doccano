#!/usr/bin/env bash

set -o errexit

if [[ -z "${ADMIN_USERNAME}" ]]; then echo "Missing ADMIN_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_PASSWORD}" ]]; then echo "Missing ADMIN_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_EMAIL}" ]]; then echo "Missing ADMIN_EMAIL environment variable" >&2; exit 1; fi

set -o nounset

app="/src/backend"

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
python -u "${app}/manage.py" runserver ${HOST:-0.0.0.0}:${PORT:-8000}
