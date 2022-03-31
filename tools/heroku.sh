#!/usr/bin/env bash

set -o errexit

if [[ -z "${ADMIN_USER_NAME}" ]]; then echo "Missing ADMIN_USER_NAME environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_PASSWORD}" ]]; then echo "Missing ADMIN_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "${ADMIN_CONTACT_EMAIL}" ]]; then echo "Missing ADMIN_CONTACT_EMAIL environment variable" >&2; exit 1; fi

set -o nounset

python /doccano/backend/manage.py migrate
if [ -n "$ADMIN_USER_NAME" ]; then
    python /doccano/backend/manage.py create_admin --noinput --username="$ADMIN_USER_NAME" --email="$ADMIN_CONTACT_EMAIL" --password="$ADMIN_PASSWORD"
fi
