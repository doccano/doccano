#!/usr/bin/env bash

set -o errexit
set -o nounset

cd "/src/backend"

(
  echo "Waiting for database"
  python manage.py wait_for_db

  echo "Starting celery"
  "watchmedo" auto-restart --directory="." --pattern="*.py" --recursive -- "celery" --app=config worker --loglevel=info --pool=solo
)
