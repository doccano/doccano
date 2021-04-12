#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

sed -i 's^dockerfile: app/Dockerfile.prod^dockerfile: app/Dockerfile.prod\n    image: doccano-app:custom^g' ../docker-compose.prod.yml
sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g'     ../docker-compose.prod.yml

docker-compose -f ../docker-compose.prod.yml pull
docker-compose -f ../docker-compose.prod.yml build

docker image save -o doccano-app.tar   doccano-app:custom
docker image save -o doccano-nginx.tar doccano-nginx:custom
docker image save -o postgres.tar      postgres:13.1-alpine
