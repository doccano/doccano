FROM node:13.1.0

# set work directory
WORKDIR /app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1

# copy project
COPY . /app/

# install dependencies
RUN npm install -g npm@latest
RUN npm install

# build project
RUN npm run build
RUN ls -l