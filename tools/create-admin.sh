#!/usr/bin/env bash

set -o errexit

python app/manage.py wait_for_db
python app/manage.py migrate

python app/manage.py create_admin --noinput --username="$ADMIN_USERNAME" --email="$ADMIN_EMAIL" --password="$ADMIN_PASSWORD"
