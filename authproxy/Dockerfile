FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY proxy.conf /app/proxy.conf

ENV PORT=8888
ENV PROXY_PASS=""
ENV USER_NAME=""
ENV USER_GROUPS=""

EXPOSE ${PORT}

CMD envsubst < /app/proxy.conf > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
