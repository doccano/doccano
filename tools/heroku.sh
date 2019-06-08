#!/usr/bin/env bash

set -o errexit

if [ "$1" = "build" ]; then
    cd app/server/static
    npm install --only=prod
    npm install --only=dev
    ./node_modules/.bin/webpack --config ./webpack.config.js --mode production
    echo "Done webpack build."
    ls ./bundle
else
    python app/manage.py migrate
    python app/manage.py collectstatic --noinput
    python app/manage.py create_admin --noinput --username="$ADMIN_USER_NAME" --email="$ADMIN_CONTACT_EMAIL" --password="$ADMIN_PASSWORD"

fi
