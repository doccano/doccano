docker build -t mydoccano -f ./docker/Dockerfile .

docker container create --name mydoccano -e "ADMIN_USERNAME=admin" -e "ADMIN_EMAIL=admin@example.com" -e "ADMIN_PASSWORD=password" -v doccano-db:/data -p 8000:8000 mydoccano 

docker container start mydoccano