ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION}

ARG NODE_VERSION="8.x"
RUN curl -sL "https://deb.nodesource.com/setup_${NODE_VERSION}" | bash - \
 && apt-get install nodejs \
 && rm -rf /var/lib/apt/lists/*

COPY app/server/package*.json /doccano/app/server/
RUN cd /doccano/app/server && npm ci

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY app/server/static /doccano/app/server/static/
COPY app/server/webpack.config.js /doccano/app/server/
RUN cd /doccano/app/server && DEBUG=False npm run build

COPY . /doccano

WORKDIR /doccano

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="80"
ENV WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
