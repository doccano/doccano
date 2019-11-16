FROM node:13.1.0

# set work directory
WORKDIR /app

# copy project
COPY . /app/

# install dependencies
RUN npm install -g npm@latest
RUN npm install

# build project
RUN npm run build
