ARG PYTHON_VERSION="3.6"

FROM python:${PYTHON_VERSION}

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /doccano

WORKDIR /doccano

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV BIND="0.0.0.0:80"
ENV WORKERS="2"

EXPOSE 80

CMD ["/doccano/tools/run.sh"]
