# Getting started

## Usage

Two options to run doccano:

- (Recommended) Docker Compose
- Docker

### Docker Compose

```bash
$ git clone https://github.com/doccano/doccano.git
$ cd doccano
$ docker-compose -f docker-compose.prod.yml up
```

Go to <http://0.0.0.0/>.

_Note the superuser account credentials located in the `docker-compose.prod.yml` file:_
```yml
ADMIN_USERNAME: "admin"
ADMIN_PASSWORD: "password"
```

> Note: If you want to add annotators, see [Frequently Asked Questions](https://github.com/doccano/doccano/wiki/Frequently-Asked-Questions#i-want-to-add-annotators)

_Note for Windows developers: Be sure to configure git to correctly handle line endings or you may encounter `status code 127` errors while running the services in future steps. Running with the git config options below will ensure your git directory correctly handles line endings._

```bash
git clone https://github.com/doccano/doccano.git --config core.autocrlf=input
```

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
$ git clone https://github.com/doccano/doccano.git
$ cd doccano
$ docker-compose -f docker-compose.dev.yml up
```

Go to <http://127.0.0.1:3000/>.

Or, you can setup via Python and Node.js:

### Python

```bash
$ git clone https://github.com/doccano/doccano.git
$ cd doccano/app
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py create_roles
$ python manage.py create_admin --noinput --username "admin" --email "admin@example.com" --password "password"
$ python manage.py runserver
```

### Node.js

```bash
$ cd doccano/frontend
$ yarn install
$ yarn dev
```

Go to <http://127.0.0.1:3000/>.
