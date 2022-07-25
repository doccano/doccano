#!/usr/bin/env bash

set -o errexit

if [[ -z "${ADMIN_USERNAME}" ]]; then echo "Missing ADMIN_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_PASSWORD}" ]]; then echo "Missing ADMIN_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_EMAIL}" ]]; then echo "Missing ADMIN_EMAIL environment variable" >&2; exit 1; fi

set -o nounset

python /doccano/backend/manage.py migrate
if [ -n "$ADMIN_USERNAME" ]; then
    python /doccano/backend/manage.py create_admin --noinput --username="$ADMIN_USERNAME" --email="$ADMIN_EMAIL" --password="$ADMIN_PASSWORD"
fi
