#!/usr/bin/env bash

set -o errexit

flake8
python app/manage.py migrate
coverage run --source=app app/manage.py test server.tests api.tests authentification.tests
coverage report

(cd app/server/static && npm run lint)
