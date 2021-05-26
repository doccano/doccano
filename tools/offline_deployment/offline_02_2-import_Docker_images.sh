#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# Info: Docker image name is already set in previous scripts
## Set image tag in Compose to avoid image build
#sed -i 's^dockerfile: backend/Dockerfile.prod^dockerfile: backend/Dockerfile.prod\n    image: doccano-backend:custom^g' ../../docker-compose.prod.yml
#sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g'                 ../../docker-compose.prod.yml

# Load docker images
docker image load -i doccano-backend.tar
docker image load -i doccano-nginx.tar
docker image load -i postgres.tar
docker image load -i rabbitmq.tar
