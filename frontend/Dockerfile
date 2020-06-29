FROM node:13.2-alpine3.10

WORKDIR /app

COPY . /app/

RUN apk add -U --no-cache bash git python3 make g++ \
  && npm install -g npm@latest \
  && npm install \
  && npm run build \
  && apk del --no-cache git make g++
