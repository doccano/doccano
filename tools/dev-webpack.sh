#!/usr/bin/env bash

set -o errexit

root="$(dirname "$0")/.."
server="${root}/app/server"

(
  cd "${server}"

  if [[ ! -d node_modules/.bin ]]; then
    echo "Installing dependencies"
    npm install
  fi

  echo "Starting webpack"
  npm start
)
