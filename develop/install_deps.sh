#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

# This script works only with apt package manager

apt-get update
apt-get upgrade
apt-get install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install -r requirements.txt
apt-get install -y targetcli-fb # if no targetcli presented
# apt-get install targetcli
# apt-get install -y git

# Deal with tcmu-runner

./tcmu-runner/install_dep.sh

# Start installing docker

apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install docker-ce

# Finish installing docker

# Pull docker images

# docker pull deniskoptev/lio_target


