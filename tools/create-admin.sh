#!/usr/bin/env bash

set -o errexit
set -o nounset

if [[ "$#" -ne 3 ]]; then echo "Usage: $0 <username> <email> <password>" >&2; exit 1; fi

python app/manage.py wait_for_db
python app/manage.py migrate
python app/manage.py create_admin --noinput --username="$1" --email="$2" --password="$3"
