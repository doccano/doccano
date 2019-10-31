#!/usr/bin/env bash

set -o errexit

root="$(dirname "$0")/.."
venv="${root}/venv"

while [[ ! -f "${venv}/bin/celery" ]]; do
  echo "Waiting for virtualenv"
  sleep 1
done

(
  cd "${root}/app"

  echo "Waiting for database"
  "${venv}/bin/python" manage.py wait_for_db

  echo "Starting celery"
  "${venv}/bin/watchmedo" auto-restart --directory="." --pattern="*.py" --recursive -- "${venv}/bin/celery" --app=app worker --loglevel=info --pool=solo
)
