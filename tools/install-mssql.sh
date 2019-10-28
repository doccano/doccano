#!/usr/bin/env bash

# parse arguments
mode="prod"
for opt in "$@"; do
  case "${opt}" in
    --dev) mode="dev" ;;
  esac
done

set -eo pipefail

# install build dependencies
apt-get update
apt-get install --no-install-recommends -y \
      curl=7.52.1-5+deb9u9 \
      gnupg=2.1.18-8~deb9u4 \
      apt-transport-https=1.4.9

# install dependency to compile django-pyodbc-azure
if [[ "${mode}" = "dev" ]]; then
  apt-get install --no-install-recommends -y \
      unixodbc-dev=2.3.4-1
fi

# add mssql repo
curl -fsS https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl -fsS https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql.list
apt-get update

# install mssql
ACCEPT_EULA=Y apt-get install --no-install-recommends -y \
      msodbcsql17=17.3.1.1-1 \
      mssql-tools=17.3.0.1-1

# remove build dependencies and artifacts
apt-get remove -y \
      curl gnupg apt-transport-https
rm -rf /var/lib/apt/lists/*
