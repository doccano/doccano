#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
unset DIR

# Import APT packages
pdir="/offline_packages"
abs_pdir="$(pwd)${pdir}"
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
cat <<EOF > sources.list
deb [trusted=yes] file://${abs_pdir} ./
EOF
sudo mv sources.list /etc/apt/sources.list

# Install APT packages
sudo apt-get update
SELECTED_PACKAGES="wget unzip curl tar docker.io docker-compose"
sudo apt-get install -y $SELECTED_PACKAGES

# Cleanup
sudo apt-get clean
sudo mv /etc/apt/sources.list.bak /etc/apt/sources.list

# Setup Docker
sudo usermod -aG docker $(whoami)
sudo systemctl enable docker.service

echo "Packages were installed. We need to reboot!"

