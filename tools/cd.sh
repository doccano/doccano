#!/usr/bin/env bash
function build_and_push() {
  local tag=$1
  local dir=$2

  echo "Building ${tag} from ${dir}"
  docker build -t ${tag} ${dir}

  echo "Pushing ${tag}"
  docker push ${tag}
}

if [[ -z "${DOCKER_USERNAME}" ]]; then echo "Missing DOCKER_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${DOCKER_PASSWORD}" ]]; then echo "Missing DOCKER_PASSWORD environment variable" >&2; exit 1; fi
if [[ -z "$1" ]]; then echo "Usage: $0 <tag> [<noci>]" >&2; exit 1; fi

TAG=$1
FULLCI=${2:-true}

set -o errexit

if [[ -z "${DOCKER_REGISTRY}" ]]; then
  echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin
else
  # If required, connect with a registry that is not Docker Hub
  echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin "${DOCKER_REGISTRY}"
  DOCKER_USERNAME="${DOCKER_REGISTRY}"
fi

echo "Building doccano in ${DOCKER_USERNAME}"

if [ "${FULLCI}" == "true" ]
then
  docker build -t "${DOCKER_USERNAME}/doccano:latest" .
  docker build -t "${DOCKER_USERNAME}/doccano:${TAG}" .

  docker push "${DOCKER_USERNAME}/doccano:latest"
  docker push "${DOCKER_USERNAME}/doccano:${TAG}"
fi

for component in app frontend
do
  container_name="${DOCKER_USERNAME}/doccano-${component}"
  build_and_push "${container_name}:${TAG}" $component
  build_and_push "${container_name}:latest" $component
done

