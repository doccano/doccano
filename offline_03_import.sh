#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

sed -i 's^dockerfile: app/Dockerfile.prod^dockerfile: app/Dockerfile.prod\n    image: doccano-app:custom^g' docker-compose.prod.yml
sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g' docker-compose.prod.yml

docker image import doccano-app.tar   doccano-app:custom
docker image import doccano-nginx.tar doccano-nginx:custom
docker image import postgres.tar      postgres:13.1-alpine
