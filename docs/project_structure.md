# Project Structure

The important files/directories are as follows:

```bash
/
├── app/
├── frontend/
├── nginx/
├── tools/
├── docker-compose.dev.yml
└── docker-compose.prod.yml
```

Consider them:

**[app/](https://github.com/doccano/doccano/tree/master/app)**

The `app/api` directory contains backend code. See [below](#Backend).

**[frontend/](https://github.com/doccano/doccano/tree/master/frontend)**

The `app/api` directory contains frontend code. See [below](#Frontend).

**[docker-compose.dev.yml](https://github.com/doccano/doccano/blob/master/docker-compose.dev.yml)**

The `docker-compose.dev.yml` file contains [Docker Compose](https://docs.docker.com/compose) configuration to run a development environment.
Once we run the command `docker-compose -f docker-compose.dev.yml up`, compose runs backend API and frontend development containers.

**[docker-compose.prod.yml](https://github.com/doccano/doccano/blob/master/docker-compose.prod.yml)**

The `docker-compose.prod.yml` file contains [Docker Compose](https://docs.docker.com/compose) configuration to run a production environment.
We adopted the three tier architecture. Once we run the command `docker-compose -f docker-compose.prod.yml up`, compose builds frontend and runs DBMS, backend API and web server containers.

**[nginx](https://github.com/doccano/doccano/tree/master/nginx)**

The `nginx` directory contains a NGINX configuration file and Docker container. They are used only in `docker-compose.prod.yml`.

**[tools](https://github.com/doccano/doccano/tree/master/tools)**

The `tools` directory contains some shell scripts. They are used for CI, CD and so on.

## Backend

The directory structure of the backend follows [Django](https://www.djangoproject.com) one.
The important directories are as follows:

```bash
/
├── app/
├── ├── api/
├── ├── app/
├── ├── authentification/
└── └── server/
```

**[app/api/](https://github.com/doccano/doccano/tree/master/app/api)**

The `app/api` directory contains backend API application. We use [Django Rest Framework](https://www.django-rest-framework.org) to implement the API.
If you want to add new API, change the contents of this directory.

**[app/app/](https://github.com/doccano/doccano/tree/master/app/app)**

The `app/app` directory contains Django project settings. See [Writing your first Django app, part 1](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project).

**[app/authentification/](https://github.com/doccano/doccano/tree/master/app/authentification)**

The `app/authentification` directory contains authentification application. It is mainly used for user signup.

**[app/server/](https://github.com/doccano/doccano/tree/master/app/server)**

The `app/server` directory contains doccano v0.x codes. In the future, this directory will be integrated into the `api` directory.

## Frontend

The `frontent` directory structure of the frontend follows [Nuxt.js](https://ru.nuxtjs.org) one.
See the [Nuxt.js documentation](https://nuxtjs.org/guide/directory-structure/) for details.
