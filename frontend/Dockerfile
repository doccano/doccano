FROM node:13.2-alpine

ENV NUXT_PORT 3000

CMD ["/usr/local/bin/npm", "start"]

WORKDIR /app

COPY . /app/

RUN  apk add -U --no-cache git python3 make g++ \
  && npm install -g npm@latest \
  && npm install \
  && npm run build \
  && apk del --no-cache git make g++
