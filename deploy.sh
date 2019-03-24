docker container stop doccano 
docker container rm doccano 
docker rmi doccano-stt:latest 
docker build -t doccano-stt . 
docker run -d --name doccano -p 8000:80 doccano-stt
docker exec doccano tools/create-admin.sh "admin" "admin@example.com" "admin"