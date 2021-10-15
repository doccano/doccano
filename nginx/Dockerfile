ARG NODE_VERSION="16.5-alpine3.14"
FROM node:${NODE_VERSION} AS frontend-builder

COPY frontend/ /app/
WORKDIR /app

RUN apk add -U --no-cache git python3 make g++ \
  && yarn install \
  && yarn build \
  && apk del --no-cache git make g++

FROM nginx:1.21.1-alpine AS runtime

RUN addgroup -g 61000 doccano \
  && adduser -G doccano -S doccano -u 61000

COPY --chown=doccano:doccano --from=frontend-builder /app/dist /var/www/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

RUN chown -R doccano:doccano /var/cache/nginx \
  && chmod -R g+w /var/cache/nginx \
  && chown -R doccano:doccano /media

EXPOSE 8080

USER doccano:doccano
