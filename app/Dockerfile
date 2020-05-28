FROM python:3.6

ENV LISTEN_PORT 8000
ENV WORKERS 1

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$LISTEN_PORT --workers $WORKERS --pythonpath app app.wsgi --timeout 300"]

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-dev libpq-dev unixodbc-dev \
    && mkdir -p /app/staticfiles \
    && chmod 777 /app/staticfiles

# install dependencies
RUN pip install --upgrade pip setuptools
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/
