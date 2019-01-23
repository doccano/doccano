ARG PYTHON_VERSION="3.6"

FROM python:${PYTHON_VERSION}

COPY requirements.txt /
RUN python -m venv /venv \
 && /venv/bin/pip install --no-cache-dir -r /requirements.txt

COPY . /doccano

WORKDIR /doccano

CMD ["/venv/bin/gunicorn", "--bind=0.0.0.0:80", "--workers=2", "--pythonpath=app", "app.wsgi"]
