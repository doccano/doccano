!#/bin/bash

# systemctl start docker
sudo docker-compose -f docker/docker-compose.prod.yml --env-file docker/.env up --build
