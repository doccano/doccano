#!/usr/bin/env bash

set -o errexit

python /doccano/backend/manage.py migrate
if [ -n "$ADMIN_USER_NAME" ]; then
    python /doccano/backend/manage.py create_admin --noinput --username="$ADMIN_USER_NAME" --email="$ADMIN_CONTACT_EMAIL" --password="$ADMIN_PASSWORD"
fi
