FROM node:13.2-alpine

WORKDIR /app

COPY . /app/

RUN apk add -U git python3 make g++ \
  && npm install -g npm@latest \
  && npm install \
  && npm run build \
  && apk del git make g++
