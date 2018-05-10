#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

# This script works only with apt package manager

apt-get update
apt-get upgrade -y
apt-get install -y python3 python3-pip
apt-get install -y python python-pip
#pip3 install --upgrade pip # Hack
pip install -r requirements.txt # Hack
#pip install --upgrade pip # Hack
pip install jsonschema # Hack

apt-get install -y targetcli-fb

if [ $? -ne 0 ]; then
    apt-get install -y targetcli
fi

# Deal with tcmu-runner

./tcmu-runner/install_dep.sh

# Temp initiator deps
apt-get install -y open-iscsi
apt-get install -y lsscsi

