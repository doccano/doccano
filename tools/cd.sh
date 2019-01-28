#!/usr/bin/env bash

if [[ -z "${DOCKER_USERNAME}" ]]; then echo "Missing DOCKER_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${DOCKER_PASSWORD}" ]]; then echo "Missing DOCKER_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "${TRAVIS_TAG}" ]]; then echo "Missing TRAVIS_TAG environment variable" >&2; exit 1; fi

set -o errexit

docker build -t "${DOCKER_USERNAME}/doccano:latest" .
docker build -t "${DOCKER_USERNAME}/doccano:${TRAVIS_TAG}" .

echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin

docker push "${DOCKER_USERNAME}/doccano:latest"
docker push "${DOCKER_USERNAME}/doccano:${TRAVIS_TAG}"
