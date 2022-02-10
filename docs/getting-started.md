# Getting started

## Usage

doccano has two options to run:

- (Recommended) Docker Compose
- Docker

The usage of docker compose version is explained in the [README.md](https://github.com/doccano/doccano/blob/master/README.md#usage). We highly recommend that you should use docker compose version. However, we explain the usage of Docker version and Python/Node version for the additional information.

### Docker

As a one-time setup, create a Docker container for Doccano:

```bash
docker pull doccano/doccano
docker container create --name doccano \
  -e "ADMIN_USERNAME=admin" \
  -e "ADMIN_EMAIL=admin@example.com" \
  -e "ADMIN_PASSWORD=password" \
  -p 8000:8000 doccano/doccano
```

Next, start Doccano by running the container:

```bash
docker container start doccano
```

To stop the container, run `docker container stop doccano -t 5`.
All data created in the container will persist across restarts.

Go to <http://127.0.0.1:8000/>.

### For Developers

You can setup local development environment as follows:

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
docker-compose -f docker-compose.dev.yml up
```

Go to <http://127.0.0.1:3000/>.

Or, you can setup via Python and Node.js:

### Python

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
pipenv sync --dev
pipenv shell
cd backend
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

### Node.js

```bash
cd frontend
yarn install
yarn dev
```

Go to <http://127.0.0.1:3000/>.
