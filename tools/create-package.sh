#!/usr/bin/env bash
mkdir -p backend/client

cd frontend
export PUBLIC_PATH="/static/_nuxt/"
yarn build
cp -r dist ../backend/client/

cd ../backend
poetry run task collectstatic
poetry build
