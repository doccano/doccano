ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION}-stretch AS builder

ARG NODE_VERSION="8.x"
RUN curl -sL "https://deb.nodesource.com/setup_${NODE_VERSION}" | bash - \
 && apt-get install --no-install-recommends -y \
      nodejs=8.16.0-1nodesource1

RUN apt-get install --no-install-recommends -y \
      unixodbc-dev=2.3.4-1

COPY app/server/static/package*.json /doccano/app/server/static/
RUN cd /doccano/app/server/static \
 && npm ci

COPY requirements.txt /
RUN pip install -r /requirements.txt \
 && pip wheel -r /requirements.txt -w /deps

COPY . /doccano

WORKDIR /doccano
RUN tools/ci.sh

FROM builder AS cleaner

RUN cd /doccano/app/server/static \
 && SOURCE_MAP=False DEBUG=False npm run build \
 && rm -rf components pages node_modules .*rc package*.json webpack.config.js

RUN cd /doccano \
 && python app/manage.py collectstatic --noinput

FROM python:${PYTHON_VERSION}-slim-stretch AS runtime

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      curl=7.52.1-5+deb9u9 \
      gnupg=2.1.18-8~deb9u4 \
      apt-transport-https=1.4.9 \
 && curl -fsS https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl -fsS https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install --no-install-recommends -y \
      msodbcsql17=17.3.1.1-1 \
      mssql-tools=17.3.0.1-1 \
 && apt-get remove -y curl gnupg apt-transport-https \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/sh doccano

COPY --from=builder /deps /deps
RUN pip install --no-cache-dir /deps/*.whl

COPY --from=cleaner --chown=doccano:doccano /doccano /doccano

ENV DEBUG="True"
ENV SECRET_KEY="change-me-in-production"
ENV PORT="8000"
ENV WORKERS="2"
ENV GOOGLE_TRACKING_ID=""
ENV AZURE_APPINSIGHTS_IKEY=""

USER doccano
WORKDIR /doccano
EXPOSE ${PORT}

CMD ["/doccano/tools/run.sh"]
