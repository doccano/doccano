# Project Structure

The important files/directories are as follows:

```
/
├── backend/
├── frontend/
├── nginx/
├── tools/
├── docker-compose.dev.yml
└── docker-compose.prod.yml
```

Consider them:

**[backend/](https://github.com/doccano/doccano/tree/master/backend)**

The `backend/` directory contains backend code. See [below](#Backend).

**[frontend/](https://github.com/doccano/doccano/tree/master/frontend)**

The `frontend/` directory contains frontend code. See [below](#Frontend).

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

Also, there are directories and files contain doccano v0.x codes.
In the future, they will be integrated into the current code or removed:

```
/
├── backend/
├── └── server/
```

## Backend

The directory structure of the backend follows [Django](https://www.djangoproject.com) one.
The important directories are as follows:

```
/
├── backend/
├── ├── api/
├── ├── app/
└── └── authentification/
```

**[backend/api/](https://github.com/doccano/doccano/tree/master/backend/api)**

The `backend/api` directory contains backend API application. We use [Django Rest Framework](https://www.django-rest-framework.org) to implement the API.
If you want to add new API, change the contents of this directory.

**[backend/app/](https://github.com/doccano/doccano/tree/master/backend/app)**

The `backend/app` directory contains Django project settings. See [Writing your first Django app, part 1](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project).

**[backend/authentification/](https://github.com/doccano/doccano/tree/master/backend/authentification)**

The `backend/authentification` directory contains authentification application. It is mainly used for user signup.

## Frontend

The `frontent` directory structure of the frontend follows [Nuxt.js](https://ru.nuxtjs.org) one.
See the [Nuxt.js documentation](https://nuxtjs.org/guide/directory-structure/) for details.
