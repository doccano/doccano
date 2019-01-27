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
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

EXPOSE 80

CMD ["/doccano/tools/run.sh"]
