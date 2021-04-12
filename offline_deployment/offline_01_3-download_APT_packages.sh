#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# Prepare and download packages
pdir="/offline_packages"
mkdir -p "$(pwd)${pdir}"
cd "$(pwd)${pdir}"

SELECTED_PACKAGES="wget unzip curl tar docker.io docker-compose"

apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
  --no-conflicts --no-breaks --no-replaces --no-enhances \
  --no-pre-depends ${SELECTED_PACKAGES} | grep "^\w")

# Build package index
sudo apt-get install -y dpkg-dev
dpkg-scanpackages "." /dev/null | gzip -9c > Packages.gz

echo "Packages extracted to: $(pwd)${pdir}"