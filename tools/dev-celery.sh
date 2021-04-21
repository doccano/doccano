#!/usr/bin/env bash
set -o errexit

app="/src/backend"
cd "/src/backend"

(
  echo "Waiting for database"
  python manage.py wait_for_db

  echo "Starting celery"
  "watchmedo" auto-restart --directory="." --pattern="*.py" --recursive -- "celery" --app=app worker --loglevel=info --pool=solo
)
