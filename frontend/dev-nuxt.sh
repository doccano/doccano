#!/usr/bin/env bash

set -o errexit

root="$(dirname "$0")/.."
app="${root}/frontend"

(
  cd "${app}"
 
  if [[ ! -d node_modules/.bin ]]; then
    echo "Installing dependencies"
    yarn install
  fi

  echo "Starting frontend server"
  yarn lintfix
  yarn dev
)
