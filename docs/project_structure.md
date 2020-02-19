# Project Structure

In doccano v1.x, the application consists of a frontend and backend API. They are stored in the `frontend` and `app` directories.

```bash
.
├── app
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── frontend
├── nginx
└── tools
```

The other important files/directories are as follows:

- [docker-compose.dev.yml](https://github.com/doccano/doccano/blob/master/docker-compose.dev.yml)
- [docker-compose.prod.yml](https://github.com/doccano/doccano/blob/master/docker-compose.prod.yml)
- [nginx](https://github.com/doccano/doccano/tree/master/nginx)
- [tools](https://github.com/doccano/doccano/tree/master/tools)

**[docker-compose.dev.yml](https://github.com/doccano/doccano/blob/master/docker-compose.dev.yml)**

The `docker-compose.dev.yml` file contains configuration to run a development environment. Once we run the command `docker-compose -f docker-compose.dev.yml up`, compose runs backend API and frontend development containers.

**[docker-compose.prod.yml](https://github.com/doccano/doccano/blob/master/docker-compose.prod.yml)**

The `docker-compose.prod.yml` file contains configuration to run a production environment. We adopted the three tier architecture. Once we run the command `docker-compose -f docker-compose.prod.yml up`, compose builds frontend and runs DBMS, backend API and web server containers.

**[nginx](https://github.com/doccano/doccano/tree/master/nginx)**

The `nginx` directory contains a nginx configuration file and Docker container. They are used only in `docker-compose.prod.yml`.

**[tools](https://github.com/doccano/doccano/tree/master/tools)**

The `tools` directory contains some shell scripts. They are used for CI, CD and so on.

## Frontend

The directory structure of the frontend follows Nuxt.js one. See the Nuxt.js documentation for details:

- [Nuxt.js/Directory Structure](https://nuxtjs.org/guide/directory-structure/)


## Backend API

The directory structure of the backend api follows Django one. The important directories are as follows:

```bash
.
├── api
├── app
├── authentification
└── server
```

**[app/api](https://github.com/doccano/doccano/tree/master/app/api)**

The `api` directory contains backend API application. We use Django Rest Framework to implement the API. If you want to add new API, change the contents of this directory.

**[app/app](https://github.com/doccano/doccano/tree/master/app/app)**

The `app` directory contains Django project settings. See [Writing your first Django app, part 1](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project).

**[app/authentification](https://github.com/doccano/doccano/tree/master/app/authentification)**

The `authentification` directory contains authentification application. It is mainly used for user signup.

**[app/server](https://github.com/doccano/doccano/tree/master/app/server)**

The `server` directory contains doccano v0.x codes. In the future, this directory will be integrated into the `api` directory.
