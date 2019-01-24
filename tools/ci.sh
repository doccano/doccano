#!/usr/bin/env bash

set -o errexit

python app/manage.py migrate
python app/manage.py collectstatic
python app/manage.py test server.tests
