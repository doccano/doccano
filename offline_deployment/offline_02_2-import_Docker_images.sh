#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# Set image tag in Compose to avoid image build
sed -i 's^dockerfile: app/Dockerfile.prod^dockerfile: app/Dockerfile.prod\n    image: doccano-app:custom^g' ../docker-compose.prod.yml
sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g' ../docker-compose.prod.yml

# Load docker images
docker image load -i doccano-app.tar
docker image load -i doccano-nginx.tar
docker image load -i postgres.tar
