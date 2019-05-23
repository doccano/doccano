ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION} AS builder

ARG NODE_VERSION="8.x"
RUN curl -sL "https://deb.nodesource.com/setup_${NODE_VERSION}" | bash - \
 && apt-get install nodejs

COPY app/server/static/package*.json /doccano/app/server/static/
RUN cd /doccano/app/server/static \
 && npm ci

COPY requirements.txt /
RUN pip install -r /requirements.txt \
 && pip wheel -r /requirements.txt -w /deps

COPY . /doccano

RUN cd /doccano \
 && tools/ci.sh

FROM builder AS cleaner

RUN cd /doccano/app/server/static \
 && SOURCE_MAP=False DEBUG=False npm run build \
 && rm -rf components pages node_modules .*rc package*.json webpack.config.js

RUN cd /doccano \
 && python app/manage.py collectstatic --noinput

FROM python:${PYTHON_VERSION}-slim AS runtime

COPY --from=builder /deps /deps
RUN pip install --no-cache-dir /deps/*.whl

COPY --from=cleaner /doccano /doccano

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="80"
ENV WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

WORKDIR /doccano
EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
