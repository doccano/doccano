#!/usr/bin/env bash

set -o errexit

flake8
python app/manage.py migrate
python app/manage.py collectstatic
python app/manage.py test server.tests
