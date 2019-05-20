#!/usr/bin/env bash

set -o errexit

if [[ -z "${DOCCANO_LOCATION}" ]]; then echo "Missing DOCCANO_LOCATION environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_RESOURCE_GROUP}" ]]; then echo "Missing DOCCANO_LOCATION environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_APP_NAME}" ]]; then echo "Missing DOCCANO_APP_NAME environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_SECRET_KEY}" ]]; then echo "Missing DOCCANO_SECRET_KEY environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_ADMIN_USERNAME}" ]]; then echo "Missing DOCCANO_ADMIN_USERNAME environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_ADMIN_CONTACT_EMAIL}" ]]; then echo "Missing DOCCANO_ADMIN_CONTACT_EMAIL environment variable" >&2; exit 1; fi
if [[ -z "${DOCCANO_ADMIN_PASSWORD}" ]]; then echo "Missing DOCCANO_ADMIN_PASSWORD environment variable" >&2; exit 1; fi
if ! az account show >/dev/null; then echo "Must be logged into Azure" >&2; exit 2; fi

az group create \
  --location "${DOCCANO_LOCATION}" \
  --name "${DOCCANO_RESOURCE_GROUP}"

az group deployment create \
  --resource-group "${DOCCANO_RESOURCE_GROUP}" \
  --name "azuredeploy$1" \
  --parameters \
      appName="${DOCCANO_APP_NAME}" \
      secretKey="${DOCCANO_SECRET_KEY}" \
      adminUserName="${DOCCANO_ADMIN_USERNAME}" \
      adminContactEmail="${DOCCANO_ADMIN_CONTACT_EMAIL}" \
      adminPassword="${DOCCANO_ADMIN_PASSWORD}" \
      dockerImageName="${DOCKER_REGISTRY:-${DOCKER_USERNAME:-chakkiworks}}/doccano:${1:-latest}" \
      dockerRegistry="${DOCKER_REGISTRY}" \
      dockerRegistryUserName="${DOCKER_USERNAME}" \
      dockerRegistryPassword="${DOCKER_PASSWORD}" \
  --template-file azuredeploy.json
