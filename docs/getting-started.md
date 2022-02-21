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

### Setup development environment

You can setup development environment via Python and Node.js. You need to install Git and to clone the repository:

```bash
git clone https://github.com/doccano/doccano.git
cd doccano
```

### Backend

The doccano backend is built in Python 3.8+ and uses [Poetry](https://github.com/python-poetry/poetry) as a dependency manager. If you haven't installed them yet, please see [Python](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/) documentation.

First, to install the defined dependencies for our project, just run the `install` command. After that, activate the virtual environment by runnning `shell` command:

```bash
cd backend
poetry install
poetry shell
```

Second, setup database and run the development server. Doccano uses [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/) as a backend. We can setup them by using Django command:

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

After you change the code, don't forget to run [mypy](https://mypy.readthedocs.io/en/stable/index.html), [flake8](https://flake8.pycqa.org/en/latest/), [black](https://github.com/psf/black), and [isort](https://github.com/PyCQA/isort). These ensures the code consistency. To run them, just run the following commands:

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

## How to create a Python package

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
