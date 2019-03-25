ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION} AS builder

ARG NODE_VERSION="8.x"
RUN curl -sL "https://deb.nodesource.com/setup_${NODE_VERSION}" | bash - \
 && apt-get install nodejs \
 && rm -rf /var/lib/apt/lists/*

COPY app/server/package*.json /doccano/app/server/
RUN cd /doccano/app/server \
 && npm ci

COPY requirements.txt /
RUN pip install -r /requirements.txt \
 && pip wheel -r /requirements.txt -w /deps

COPY app/server/static /doccano/app/server/static/
COPY app/server/webpack.config.js /doccano/app/server/
RUN cd /doccano/app/server \
 && DEBUG=False npm run build \
 && rm -rf node_modules/

COPY . /doccano

FROM python:${PYTHON_VERSION}-slim AS runtime

COPY --from=builder /deps /deps
RUN pip install --no-cache-dir /deps/*.whl

COPY --from=builder /doccano /doccano

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="80"
ENV WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

WORKDIR /doccano
EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
