#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
cd ../..
unset DIR

# create certificate pair
sudo apt-get install -y openssl
openssl req -new -newkey rsa:4096 -sha256 -nodes -x509 -keyout ./nginx/cert.key -out ./nginx/cert.crt \
   -subj "/C=US/ST=StateCode/L=LocationName/O=OrganizationName/OU=OrganizationUnit/CN=doccano.herokuapp.com"

# define cert paths inside container
ssl_cert="/certs/cert.crt"
ssl_cert_key="/certs/cert.key"

# edit default.conf
sed -i "s|listen 80;|listen 443 ssl;\n    ssl_certificate $ssl_cert;\n    ssl_certificate_key $ssl_cert_key;|g" nginx/default.conf

# edit nginx Dockerfile
echo "RUN mkdir -p /certs/"                >> nginx/Dockerfile
echo "COPY nginx/cert.key /certs/cert.key" >> nginx/Dockerfile
echo "COPY nginx/cert.crt /certs/cert.crt" >> nginx/Dockerfile

# edit published port
sed -i "s|- 80:80|- 443:443|g" docker-compose.prod.yml

echo "Switched to HTTPS"
