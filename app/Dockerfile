FROM alpine:3.9.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LISTEN_PORT 8000
ENV WORKERS 1

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$LISTEN_PORT --workers $WORKERS --pythonpath app app.wsgi --timeout 300"]

WORKDIR /app
COPY . /app/

RUN apk add -U --no-cache bash python3 python3-dev libpq postgresql-dev unixodbc-dev musl-dev g++ libffi-dev \
  && pip3 install --upgrade --no-cache-dir pip setuptools \
  && pip3 install --no-cache-dir -r requirements.txt \
  && ln -s /usr/bin/python3 /usr/bin/python \
  && apk del --no-cache python3-dev postgresql-dev unixodbc-dev musl-dev g++ libffi-dev \
  && mkdir -p /app/staticfiles \
  && chmod 777 /app/staticfiles

