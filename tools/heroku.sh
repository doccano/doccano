#!/usr/bin/env bash

set -o errexit

if [ -n "$ADMIN_USER_NAME" ]; then
    python app/manage.py create_admin --noinput --username="$ADMIN_USER_NAME" --email="$ADMIN_CONTACT_EMAIL" --password="$ADMIN_PASSWORD"
fi
