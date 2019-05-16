#!/usr/bin/env bash

if [[ -z "${DOCKER_USERNAME}" ]]; then echo "Missing DOCKER_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${DOCKER_PASSWORD}" ]]; then echo "Missing DOCKER_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "$1" ]]; then echo "Usage: $0 <tag>" >&2; exit 1; fi

set -o errexit

if [[ -z "${DOCKER_REGISTRY}" ]]; then
  echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin
else
  echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin "${DOCKER_REGISTRY}"
  DOCKER_USERNAME="${DOCKER_REGISTRY}"
fi

docker build -t "${DOCKER_USERNAME}/doccano:latest" .
docker build -t "${DOCKER_USERNAME}/doccano:$1" .

docker push "${DOCKER_USERNAME}/doccano:latest"
docker push "${DOCKER_USERNAME}/doccano:$1"
