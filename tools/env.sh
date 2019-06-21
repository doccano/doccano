#!/bin/bash

export ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
export ADMIN_PASSWORD=${ADMIN_PASSWORD:-password}
export ADMIN_EMAIL=${ADMIN_EMAIL:-admin@example.com}
export DATABASE_URL=${DATABASE_URL:-postgres://doccano:doccano@localhost:5432/doccano?sslmode=disable}

$@
