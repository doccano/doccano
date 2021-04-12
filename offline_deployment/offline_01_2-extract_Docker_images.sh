#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# WORKAROUND: Downgrade docker-compose version to match Ubuntu 18.04 default compose package
echo "Patching docker-compose to match Ubuntu 18.04 compose package"
sed -i 's|version: "3.7"|version: "3.3"|g' ../docker-compose.prod.yml

sed -i 's^dockerfile: app/Dockerfile.prod^dockerfile: app/Dockerfile.prod\n    image: doccano-app:custom^g' ../docker-compose.prod.yml
sed -i 's^dockerfile: nginx/Dockerfile^dockerfile: nginx/Dockerfile\n    image: doccano-nginx:custom^g'     ../docker-compose.prod.yml

docker-compose -f ../docker-compose.prod.yml pull
docker-compose -f ../docker-compose.prod.yml build

docker image save -o doccano-app.tar   doccano-app:custom
docker image save -o doccano-nginx.tar doccano-nginx:custom
docker image save -o postgres.tar      postgres:13.1-alpine
