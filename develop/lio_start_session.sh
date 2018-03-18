#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo "[ERROR] This script must be run as root" 1>&2
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "[ERROR] Invalid count of arguments"
    echo "[INFO] Usage: ./lio_start_session.sh /path/to/config.json"
fi

if [ -d "./session" ]; then
    echo "[INFO] Previous session directory exists. It will be recreated."
    rm -rf ./session
fi

mkdir ./session

echo "[INFO] Python3 location: "
which python3

if [ $? -eq 0 ]; then
    echo "[INFO] Using installed python3 package"
else
    echo "[Warning] Python3 is not installed. Trying to install."
    apt-get install -y python3
fi


