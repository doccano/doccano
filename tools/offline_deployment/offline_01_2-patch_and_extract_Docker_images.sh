#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# WORKAROUND: Downgrade docker-compose version to match Ubuntu 18.04 default compose package
echo "Patching docker-compose to match Ubuntu 18.04 compose package"
sed -i 's|version: "3.7"|version: "3.3"|g' ../../docker-compose.prod.yml

sed -i 's^dockerfile: backend/Dockerfile.prod^dockerfile: backend/Dockerfile.prod\n    image: doccano-backend:custom^g' ../../docker-compose.prod.yml
sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g'                 ../../docker-compose.prod.yml

# Modify Dockerfile for nginx to add python3 and offline patch
sed -i 's|FROM nginx|COPY tools/offline_deployment/offline_patcher.py /patch.py\
RUN apk add -U --no-cache py3-requests \\\
  \&\& mkdir -p /app/dist/offline \&\& python3 /patch.py /app/dist /app/dist/offline /offline\
\
FROM nginx|' ../../nginx/Dockerfile

# Modify Dockerfile for backend to add python3 and offline patch
# TODO: Remark: Not needed due to SPA frontend
#sed -i 's|COPY ./Pipfile\* /backend/|COPY ./Pipfile\* /backend/\
#COPY tools/offline_deployment/offline_patcher.py /patch.py\
#RUN apt-get update \
#  \&\& apt-get install -y --no-install-recommends \
#       python3 python3-requests \
#  \&\& apt-get clean \\\
#  \&\& rm -rf /var/lib/apt/lists/\*\
#  \&\& mkdir -p /backend/server/static/offline \&\& python3 /patch.py /backend/server /server/static/offline\
#\
#|' ../../backend/Dockerfile.prod

docker-compose -f ../../docker-compose.prod.yml pull
docker-compose -f ../../docker-compose.prod.yml build

docker image save -o doccano-backend.tar doccano-backend:custom
docker image save -o doccano-nginx.tar   doccano-nginx:custom
docker image save -o postgres.tar        postgres:13.1-alpine
docker image save -o rabbitmq.tar        rabbitmq:3.8
