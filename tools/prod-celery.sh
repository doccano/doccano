#!/usr/bin/env bash
set -o errexit

cd /backend

(
  echo "Waiting for database"
  python manage.py wait_for_db

  echo "Starting celery"
  "celery" --app=app worker --loglevel=info --pool=solo
)
