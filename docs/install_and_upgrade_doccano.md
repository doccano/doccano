# Install doccano

Install doccano on local or in the cloud. Choose the installation method that works best for your environment:

- [Install doccano](#install-doccano)
  - [System requirements](#system-requirements)
    - [Web browser support](#web-browser-support)
    - [Port requirements](#port-requirements)
  - [Install with pip](#install-with-pip)
    - [Use PostgreSQL as a database](#use-postgresql-as-a-database)
    - [Use RabbitMQ as a message broker](#use-rabbitmq-as-a-message-broker)
    - [Use Flower to monitor Celery tasks](#use-flower-to-monitor-celery-tasks)
  - [Install with Docker](#install-with-docker)
    - [Build a local image with Docker](#build-a-local-image-with-docker)
    - [Use Flower](#use-flower)
  - [Install with Docker Compose](#install-with-docker-compose)
  - [Install from source](#install-from-source)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [How to create a Python package](#how-to-create-a-python-package)
  - [Install to cloud](#install-to-cloud)
  - [Upgrade doccano](#upgrade-doccano)
    - [After v1.6.0](#after-v160)
    - [Before v1.6.0](#before-v160)

## System requirements

You can install doccano on a Linux, Windows, or macOS machine running Python 3.8+.

### Web browser support

doccano is tested with the latest version of Google Chrome and is expected to work in the latest versions of:

- Google Chrome
- Apple Safari

If using other web browsers, or older versions of supported web browsers, unexpected behavior could occur.

### Port requirements

doccano uses port 8000 by default. To use a different port, specify it when running doccano webserver.

## Install with pip

To install doccano with pip, you need Python 3.8+. Run the following:

```bash
pip install doccano
```

After you install doccano, start the server with the following command:

```bash
# Initialize database. First time only.
doccano init
# Create a super user. First time only.
doccano createuser --username admin --password pass
# Start a web server.
doccano webserver --port 8000
```

In another terminal, run the following command:

```bash
# Start the task queue to handle file upload/download.
doccano task
```

Open <http://localhost:8000/>.

### Use PostgreSQL as a database

By default, SQLite 3 is used for the default database system. You can also use other database systems like PostgreSQL, MySQL, and so on. Here we will show you how to use PostgreSQL.

First, you need to install `psycopg2-binary` as an additional dependency:

```bash
pip install psycopg2-binary
```

Next, set up PostgreSQL. You can set up PostgreSQL directly, but here we will use Docker. Let's run the `docker run` command with the user name(`POSTGRES_USER`), password(`POSTGRES_PASSWORD`), and database name(`POSTGRES_DB`). For other options, please refer to the [official documentation](https://hub.docker.com/_/postgres).

```bash
docker run -d \
  --name doccano-postgres \
  -e POSTGRES_USER=doccano_admin \
  -e POSTGRES_PASSWORD=doccano_pass \
  -e POSTGRES_DB=doccano \
  -v doccano-db:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13.8-alpine
```

Then, set `DATABASE_URL` environment variable according to your PostgreSQL credentials. The schema is in line with dj-database-url. Please refer to the [official documentation](https://github.com/jazzband/dj-database-url) for the detailed information.

```bash
# export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}?sslmode=disable"
export DATABASE_URL="postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable"
```

That's it. Now you can start by running the `doccano init` command.

### Use RabbitMQ as a message broker

doccano uses Celery and a message broker to handle long tasks like importing/exporting datasets. By default, SQLite3 is used for the default message broker. You can also use other message brokers like RabbitMQ, Redis, and so on. Here we will show you how to use RabbitMQ.

First, set up RabbitMQ. You can set up RabbitMQ directly, but here we will use Docker. Let's run the `docker run` command with the user name(`RABBITMQ_DEFAULT_USER`), password(`RABBITMQ_DEFAULT_PASS`). For other options, please refer to the [official documentation](https://hub.docker.com/_/rabbitmq).

```bash
docker run -d \
  --hostname doccano \
  --name doccano-rabbit \
  -e RABBITMQ_DEFAULT_USER=doccano_rabit \
  -e RABBITMQ_DEFAULT_PASS=doccano_pass \
  -p 5672:5672 \
  rabbitmq:3.10.7-alpine
```

Then, set `CELERY_BROKER_URL` environment variable according to your RabbitMQ credentials. If you want to know the schema, please refer to the [official documentation](https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-settings).

```bash
# export CELERY_BROKER_URL='amqp://${RABBITMQ_DEFAULT_USER}:${RABBITMQ_DEFAULT_PASS}@localhost:5672//'
export CELERY_BROKER_URL='amqp://doccano_rabit:doccano_pass@localhost:5672//'
```

That's it. Now you can start webserver and task queue by running the `doccano webserver` and `doccano task` command. Notice that the both commands needs `DATABASE_URL` and `CELERY_BROKER_URL` environment variables if you would change them.

### Use Flower to monitor Celery tasks

If you want to monitor and manage celery tasks, you can use [Flower](https://flower.readthedocs.io/en/latest/index.html). The `–basic_auth` option accepts _user:password_ pairs separated by a comma. If configured, any client trying to access this Flower instance will be prompted to provide the credentials specified in this argument:

```bash
doccano flower --basic_auth=user1:password1,user2:password2
```

Open <http://localhost:5555/>.

## Install with Docker

doccano is also available as a [Docker](https://www.docker.com/) container. Make sure you have Docker installed on your machine.

To install and start doccano at <http://localhost:8000>, run the following command:

```bash
docker pull doccano/doccano
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -v doccano-db:/data \
  -p 8000:8000 doccano/doccano
```

Next, start doccano by running the container:

```bash
docker container start doccano
```

To stop the container, run `docker container stop doccano -t 5`.
All data created in the container persist across restarts.

If you want to use the latest features, please specify `nightly` tag:

```bash
docker pull doccano/doccano:nightly
```

### Build a local image with Docker

If you want to build a local image, run:

```bash
docker build -t doccano:latest . -f docker/Dockerfile
```

### Use Flower

Set `FLOWER_BASIC_AUTH` environment variable and open `5555` port. The variable accepts _user:password_ pairs separated by a comma.

```bash
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -e "FLOWER_BASIC_AUTH=username:password"
  -v doccano-db:/data \
  -p 8000:8000 -p 5555:5555 doccano/doccano
```

## Install with Docker Compose

You need to install Git and to clone the repository:

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
```

To install and start doccano at <http://localhost>, run the following command:

```bash
cd docker
cp .env.example .env
# Edit with the editor of your choice, in this example nano is used (ctrl+x, then "y" to save).
nano .env
docker-compose -f docker-compose.prod.yml --env-file .env up
```

You can override the default setting by rewriting the `.env` file. See [./docker/.env.example](https://github.com/doccano/doccano/blob/master/docker/.env.example) in detail.

## Install from source

If you want to develop doccano, consider downloading the source code using Git and running doccano locally. First of all, clone the repository:

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
```

### Backend

The doccano backend is built in Python 3.8+ and uses [Poetry](https://github.com/python-poetry/poetry) as a dependency manager. If you haven't installed them yet, please see [Python](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/) documentation.

First, to install the defined dependencies for our project, just run the `install` command. After that, activate the virtual environment by running `shell` command:

```bash
cd backend
poetry install
poetry shell
```

Second, set up the database and run the development server. Doccano uses [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/) as a backend. We can set up them by using Django command:

```bash
python manage.py migrate
python manage.py create_roles
python manage.py create_admin --noinput --username "admin" --email "admin@example.com" --password "password"
python manage.py runserver
```

In another terminal, you need to run Celery to use import/export dataset feature:

```bash
cd doccano/backend
celery --app=config worker --loglevel=INFO --concurrency=1
```

After you change the code, don't forget to run [mypy](https://mypy.readthedocs.io/en/stable/index.html), [flake8](https://flake8.pycqa.org/en/latest/), [black](https://github.com/psf/black), and [isort](https://github.com/PyCQA/isort). These ensure code consistency. To run them, just run the following commands:

```bash
poetry run task mypy
poetry run task flake8
poetry run task black
poetry run task isort
```

Similarly, you can run the test by executing the following command:

```bash
poetry run task test
```

Did you pass the test? Great!

### Frontend

The doccano frontend is built in Node.js and uses [Yarn](https://yarnpkg.com/) as a package manager. If you haven't installed them yet, please see [Node.js](https://nodejs.org/en/) and [Yarn](https://yarnpkg.com/) documentation.

First, to install the defined dependencies for our project, just run the `install` command.

```bash
cd frontend
yarn install
```

Then run the `dev` command to serve with hot reload at <localhost:3000>:

```bash
yarn dev
```

After you change the code, don't forget to run 
the following commands to ensure code consistency:

```bash
yarn lintfix
yarn precommit
yarn fix:prettier
```

### How to create a Python package

During development, you may want to create a Python package and verify it works correctly. In such a case, you can create a package by running the following command in the root directory of your project:

```bash
./tools/create-package.sh
```

This command builds the frontend, copies the files, and packages them. This will take a few minutes. After finishing the command, you will find `sdist` and `wheel` in `backend/dist`:

```bash
Building doccano (1.5.5.post335.dev0+6be6d198)
  - Building sdist
  - Built doccano-1.5.5.post335.dev0+6be6d198.tar.gz
  - Building wheel
  - Built doccano-1.5.5.post335.dev0+6be6d198-py3-none-any.whl
```

Then, you can install the package via `pip install` command:

```bash
pip install doccano-1.5.5.post335.dev0+6be6d198-py3-none-any.whl
```

## Install to cloud

doccano also supports one-click deployment to cloud providers. Click the following button, configure the environment, and access the UI.

| Service | Button |
|---------|---|
| AWS   | [![AWS CloudFormation Launch Stack SVG Button](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=doccano&templateURL=https://doccano.s3.amazonaws.com/public/cloudformation/template.aws.yaml)  |
| Heroku  | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2Fdoccano%2Fdoccano)  |

## Upgrade doccano

Caution: If you use SQLite3 as a database, upgrading the package would lose your database.

The migrate command has been supported since v1.6.0.

### After v1.6.0

To upgrade to the latest version of doccano, reinstall or upgrade using pip.

```bash
pip install -U doccano
```

If you need to update the database scheme, run the following:

```bash
doccano migrate
```

### Before v1.6.0

First, you need to copy the database file and media directory in the case of SQLite3:

```bash
mkdir -p ~/doccano
# Replace your path.
cp venv/lib/python3.8/site-packages/backend/db.sqlite3 ~/doccano/
cp -r venv/lib/python3.8/site-packages/backend/media ~/doccano/
```

Then, upgrade the package:

```bash
pip install -U doccano
```

At the end, run the migration:

```bash
doccano migrate
```
