#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

# This script works only with apt package manager

apt-get update
apt-get upgrade -y
apt-get install -y python3 python3-pip
sudo -H pip3 install --upgrade pip # Hack
sudo -H pip3 install -r requirements.txt # Hack
sudo -H pip3 install --upgrade pip # Hack
sudo -H pip3 install jsonschema # Hack

apt-get install -y targetcli-fb

if [ $? -ne 0 ]; then
    apt-get install -y targetcli
fi

# Deal with tcmu-runner

./tcmu-runner/install_dep.sh

# Temp initiator deps
apt-get install -y open-iscsi
apt-get install -y lsscsi

