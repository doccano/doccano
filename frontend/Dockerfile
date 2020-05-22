FROM node:13.2.0

ENV NUXT_PORT 3000

CMD ["/usr/local/bin/npm", "start"]

# set work directory
WORKDIR /app

# copy project
COPY . /app/

# install dependencies
RUN LAYER=build \
  && npm install -g npm@latest \
  && npm install \
  && npm run build
